import math
import time
import pandas as pd
import logging
from app.models.dfcandle import DataframeCandle
import mplfinance as mpf
import numpy as np
import settings
import gmo.apiclient as api
import constants

logger = logging.getLogger(__name__)

class Conductor(object):
  '''シグナルを発生するのための基底クラス
  このオブジェクトからapiを呼び出す
  資産残高や利益額などもこのオブジェクトで管理する。

  attributes:
    api_client: gmo.apiclient.APIPrivate
    duration: 
    balance:
    usage:
    units:
    position:
    trades:
    data:
    initial_balance:
    active_orders:
  
  =============================================================================

  methods:
    get_data(): データを取得する
    plot_chart():
    get_candle():

  
  '''
  def __init__(self, usage=1.0):
    self.api_client = api.APIPrivate(settings.apiLabel, settings.apiKey, settings.secretKey)
    self.duration = settings.tradeDuration 
    self.balance = float(self.api_client.get_balance()["data"]["equity"])
    self.usage = usage
    self.units = 0
    self.position = 0
    self.trades = 0
    self.data = None
    self.initial_balance = self.balance # 初期口座残高の保存
    self.active_orders = []

  def get_data(self, momentum):
    '''データを取得する'''
    df = DataframeCandle(self.duration)
    df.set_all_candles(limit=100)

    data = []
    for candle in df.candles:
      data.append(candle.value)

    candles = pd.DataFrame(data)
    candles['time'] = pd.to_datetime(candles['time'])
    candles['volume'] = 0
    candles['return'] = np.log(candles['close'] / candles['close'].shift(1))
    candles['momentum'] = candles['return'].rolling(momentum).mean()
    candles = candles.set_index('time')
    self.data = candles.dropna()

  def plot_chart(self, type: str = 'candle', mav=[5, 30, 120], volume=True):
    '''データをプロットする
    '''
    mpf.plot(self.data, type=type, mav=mav, volume=volume)

  def get_candle(self, index):
    '''ローソク足の価格情報を取得する
    index: pd.DataFrame内のローソク足のインデックス番号

    returns
    ====================
    date: str
    open: float
    high: float
    low: float
    close: float
    ====================
    '''
    time = str(self.data.index[index])[:16]
    open = float(self.data.iloc[index]["open"])
    high = float(self.data.iloc[index]["high"])
    low = float(self.data.iloc[index]["low"])
    close = float(self.data.iloc[index]["close"])
    return time, open, high, low, close

  def time_mid_price(self, index):
    '''ローソク足の価格情報(中間値)を取得する
    '''
    time = str(self.data.index[index])[:16]
    # mid = (float(self.data.iloc[index]['high']) + float(self.data.iloc[index]['low']) )/ 2
    time, open, high, low, close = self.get_candle(index)
    mid = (high + low) / 2
    return time, mid



  def get_equity(self):
    '''現在の評価額を取得する
    '''
    res = self.api_client.get_assets()
    equity = None

    try:
        equity = float(res["data"]["equity"])
    except KeyError as e:
        logger.error("KeyError, {e} is not found")

    return equity



  def place_buy_order(self, size=None) -> bool:
    '''新規の買い注文を発行する
    '''
    if size is None:
        # size = int(math.floor(bulk_size / 10000)) * 10000
        size = 10000
    res = self.api_client.place_buy_order(size)
    # {'status': 0, 'data': [{'executionType': 'MARKET', 'orderId': 4015908, 'orderType': 'NORMAL', 'rootOrderId': 4015908, 'settleType': 'OPEN', 'side': 'BUY', 'size': '10000', 'status': 'EXECUTED', 'symbol': 'USD_JPY', 'timestamp': '2024-03-29T08:21:25.984Z'}], 'responsetime': '2024-03-29T08:21:26.245Z'}
    print("buy_order:", res)
    if res["data"][0]["status"] == 'EXECUTED':
        execution = self.api_client.get_execution(str(res["data"][0]["orderId"]))
        # position = self.api_client.get_open_positions()
        price = float(execution["data"]["list"][0]["price"])
        self.balance -= size * price
        self.units += size 
        self.trades += 1
        self.position = 1
        self.active_orders.append(execution["data"]["list"][0]["positionId"])
        return True
    return False

  def place_sell_order(self) -> bool:
    '''新規の売り注文を発行する
    '''
    logger.info(f'action=place_sell_order: starting')
    res = self.api_client.place_sell_order(size=self.units)
    logger.info(f'action=place_sell_order: finished | res={res}')

    if res["data"][0]["status"] == 'EXECUTED':
        size = int(res["data"][0]["size"])
        logger.info(f'action=place_sell_order: get_execution() starting...')
        execution = self.api_client.get_execution(str(res["data"][0]["positionId"]))
        logger.info(f'action=place_sell_order: api_client.get_execution() finished | res={execution}')
        price = float(execution["data"]["list"][0]["price"])
        self.balance += size * price
        self.units = 0
        self.trades += 1
        self.position = 0
        self.active_orders.append(res["data"][0]["positionId"])
        return True
    else:
        return False

  def close_position(self):
      '''建玉を決済する'''
      # 決済する建玉IDを取得する
      logger.info(f'action=close_position: get_execution() starting...')
      res = self.api_client.get_open_positions()
      logger.info(f'action=close_position: get_execution() finished | res={res}')
      position_id = self.active_orders[0]
      size = str(res["data"]["list"][0]["size"])

      logger.info(f'action=close_position: close_order() starting...')
      res_close = self.api_client.close_order(position_id, size)
      logger.info(f'action=close_position: close_order() finished | res_close={res_close}')

      if res_close["data"][0]["status"] == 'EXECUTED':
          size = int(res_close["data"][0]["size"])
          price = float(res["data"]["list"][0]["price"])
          self.balance += size * price
          self.units -= size
          self.trades += 1
          self.position = 0
          self.active_orders.pop(0)
          logger.info("position closed: {0}".format(position_id))
          return True
      else:
          return False


  def close_out(self):
    '''建玉がある場合は全ての建玉を決済する'''
    res = self.api_client.get_open_positions()

    logger.info(f'action=close_out: closing out starting...')
    while len(res["data"]["list"]) > 0:
        self.close_position()
        time.sleep(2) # APIアクセスが発生するので、待機時間を設ける
    logger.info(f'action=close_out: finished')


  def check_spread(self):
    """許容できるスプレッド値か判定する"""
    current_spread = self.api_client.get_spread()
    if current_spread < constants.ALLOWED_SPREAD:
      return True
    else:
      return False

  def get_open_position(self):
      '''建玉を持っていれば、それをconductorに反映する'''
      open_positions = self.api_client.get_open_positions()
      if len(open_positions["data"]["list"]) > 0:
          position_id = self.api_client.get_open_positions()["data"]["list"][0]["positionId"]
          self.active_orders.append(int(position_id))
          self.units += int(open_positions["data"]["list"][0]["size"])
          self.position = 1

  @property
  def values(self):
      return {'equity': self.get_equity(), 'units': self.units, 'position': self.position, 'active orders': self.active_orders }




