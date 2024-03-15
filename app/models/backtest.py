import pandas as pd
from app.models.dfcandle import DataframeCandle
import mplfinance as mpf
import os
import constants

class BackTestBase(object):
  '''バックテストのための基底クラス
  


  attributes:
  ====================
    start: datetime
      start time of trading
    end: datetime
      end time of trading
    duration: str
      opts = ["1m", "5m", "1h", "1s"]
    amount: float
      trading amount in JPY
    ftc: float
      fixed transaction cost in JPY
    ptc: float
      proportional transaction cost in JPY
    position: int
      0: no position, 1: position exists
    
  ====================

  methods:
  ====================
  get_data:
    retrieves and prepares data for backtest

  ====================

  
  '''
  def __init__(self, start, end, duration, amount, ftc,  ptc):
    self.start = start
    self.end = end
    self.duration = duration
    self.amount = amount
    self.ftc = ftc
    self.ptc = ptc
    self.units = 0
    self.position = 0
    self.get_data()

  def get_data(self):
    '''データを取得する'''
    df = DataframeCandle(self.duration)
    df.set_candles_between(self.start, self.end)

    data = []
    for candle in df.candles:
      data.append(candle.value)

    candles = pd.DataFrame(data)
    candles['time'] = pd.to_datetime(candles['time'])
    candles = candles.set_index('time')
    self.data = candles.dropna()

  def get_data_from_csv(self, filename: str):
    file_path = os.path.join(constants.ROOT_PATH, "data", filename)
    raw = pd.read_csv(file_path, index_col='date')
    raw.index = pd.to_datetime(raw.index)
    raw = pd.DataFrame(raw)
    raw = raw.loc[self.start:self.end]
    self.data = raw.dropna()

    

  def plot_data(self):
    '''データをプロットする
    '''
    mpf.plot(self.data, type='candle')

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
    date = str(self.data.index[index])[:10]
    open = float(self.data.iloc[index]["open"])
    high = float(self.data.iloc[index]["high"])
    low = float(self.data.iloc[index]["low"])
    close = float(self.data.iloc[index]["close"])
    return date, open, high, low, close

  def get_date_price(self, index):
    '''ローソク足の価格情報(中間値)を取得する
    '''
    date = str(self.data.index[index])[:10]
    mid = (float(self.data.iloc[index]['high']) + float(self.data.iloc[index]['low']) )/ 2

    return date, mid



  def print_balance(self, index):
    '''現在の資金残高を取得する(足の中間値で計算)
    
    '''
    date, _  = self.get_date_price(index)
    print(f'{date} | current balance: {self.amount:.2f}')

    

  def print_net_wealth(self, index):
    '''現在の評価額を取得する
    '''
    date, mid = self.get_date_price(index)
    net_wealth = self.amount + mid * self.units
    print(f'{date} | current new wealth: {net_wealth:.2f}')

  def place_buy_order(self, index, units=None, amount=None):
    '''新規注文を発行する
    '''
    date, mid = self.get_date_price(index)
    if units is None:
      units = int(amount / mid )

    self.amount -= mid * units * (1 + self.ptc) + self.ftc
    self.units += units
    self.position = 1

    if self.verbose:
      '''実行時の情報を表示する'''
      pass

  def place_sell_order(self, index, units=None, amount=None):
    '''新規注文を発行する
    '''
    date, mid = self.get_date_price(index)
    if units is None:
      units = int(amount / mid )

    self.amount += mid * units * (1 - self.ptc) + self.ftc
    self.units -= units
    self.position = 0

    if self.verbose:
      '''実行時の情報を表示する'''
      pass


  def close_out(self, index):
    '''建玉を決済する
    
    '''
    date, mid = self.get_date_price(index)




