import requests
import settings
import hashlib
import hmac
from datetime import datetime
import time
import logging
import math
import json

logger = logging.getLogger(__name__)

class APIPublic(object):
  """todo: private APIアクセスはここに定義する"""
  pass


class APIPrivate(APIPublic):
  """
  GMO coin Private APIへのアクセスを制御するクラス
  apiClient = APIPrivate(api_label, api_key, secret_key)
  >>> apiClient.get_balance()
  0
  """

  def __init__(self, api_label, api_key, secret_key, headers=None):
    self.api_label = api_label
    self.api_key = api_key
    self.secret_key = secret_key
    self.endpoint  = 'https://forex-api.coin.z.com/private'
    

    # personal access token authorization
    self.client = requests.Session()

  # public API methods(GET)
  def get_spread(self, symbol="USD_JPY"):
    """
    response = 
    {
        "status": 0,
        "data": [
            {
                "symbol": "USD_JPY",
                "ask": "151.816",
                "bid": "151.693",
                "timestamp": "2024-04-09T20:23:59.921899Z",
                "status": "OPEN"
            }
        ],
        "responsetime": "2024-04-09T20:24:00.015Z"
    }
    
    """
    endpoint = "https://forex-api.coin.z.com/public"
    path = '/v1/ticker'
    res = requests.get(endpoint + path)
    response = res.json()
    usd_jpy_ticker = response['data'][0]
    ask = float(usd_jpy_ticker['ask'])
    bid = float(usd_jpy_ticker['bid'])
    truncated = math.floor((ask - bid) * 1000 ) / 10
    return truncated



  # authorization
  def private_authorization_get(self):
    method = "GET"
    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    text = timestamp + method + self.path 
    sign = hmac.new(bytes(settings.secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()

    headers = {
      "API-KEY": self.api_key,
      "API-TIMESTAMP": timestamp,
      "API-SIGN": sign
    }
    self.client.headers.update(headers)

  def private_authorization_post(self, timestamp, sign):
    headers = {
      "API-KEY": self.api_key,
      "API-TIMESTAMP": timestamp,
      "API-SIGN": sign
    }
    self.client.headers.update(headers)

  #=================================================#


  # private API methods(GET)

  def get_balance(self):
    '''
    {'status': 0, 'data': {'equity': '103465', 'availableAmount': '42252.6', 'balance': '100175', 'estimatedTradeFee': '0', 'margin': '61212.4', 'marginRatio': '169', 'positionLossGain': '3290', 'totalSwap': '0', 'transferableAmount': '38962'}, 'responsetime': '2024-04-10T20:13:11.611Z'}
    '''
    self.path      = '/v1/account/assets'
    self.private_authorization_get()
    res = requests.get(self.endpoint + self.path, headers=self.client.headers)
    return res.json()

  def get_open_positions(self):
    '''
    {'status': 0, 'data': {'list': [{'lossGain': '3170', 'orderedSize': '0', 'positionId': 1698733, 'price': '152.577', 'side': 'BUY', 'size': '10000', 'symbol': 'USD_JPY', 'timestamp': '2024-04-10T13:42:07.707Z', 'totalSwap': '0'}]}, 'responsetime': '2024-04-10T20:03:16.617Z'}
    '''
    self.path = '/v1/openPositions'
    self.private_authorization_get()
    res = requests.get(self.endpoint + self.path, headers=self.client.headers)
    return res.json()

  def get_execution(self, order_id: int):
    '''
    response: {'status': 0, 'data': {'list': [{'amount': '0', 'executionId': 3368298, 'fee': '0', 'lossGain': '0', 'orderId': 4015908, 'positionId': 1640914, 'price': '151.365', 'settleType': 'OPEN', 'settledSwap': '0', 'side': 'BUY', 'size': '10000', 'symbol': 'USD_JPY', 'timestamp': '2024-03-29T08:21:25.985Z'}]}, 'responsetime': '2024-03-29T08:28:07.791Z'}
    '''
    self.path = '/v1/executions'
    self.private_authorization_get()
    params = {'orderId': int(order_id)}
    res = requests.get(self.endpoint + self.path, headers=self.client.headers, params=params )
    return res.json()

  def get_assets(self):
    '''
    {'status': 0, 'data': {'availableAmount': '42147.8', 'balance': '100175', 'equity': '103355', 'estimatedTradeFee': '0', 'margin': '61207.2', 'marginRatio': '168.8', 'positionLossGain': '3180', 'totalSwap': '0', 'transferableAmount': '38967'}, 'responsetime': '2024-04-10T20:20:16.936Z'}
    '''
    self.path = '/v1/account/assets'
    self.private_authorization_get()
    res = requests.get(self.endpoint + self.path, headers=self.client.headers) 
    return res.json()

  def get_latest_executions(self):
    '''
    {
      "status": 0,
      "data": {
        "list": [
          {
            "amount":"16215.999",
            "executionId": 92123912,
            "clientOrderId": "ccccc",
            "orderId": 223456789,
            "positionId": 2234567,
            "symbol": "USD_JPY",
            "side": "SELL",
            "settleType": "CLOSE",
            "size": "10000",
            "price": "141.251",
            "lossGain": "15730",
            "fee": "-30",
            "settledSwap":"515.999",
            "timestamp": "2020-11-24T21:27:04.764Z"
          }
        ]
      },
      "responsetime": "2019-03-19T02:15:06.086Z"
    }
    '''
    self.path = '/v1/latestExecutions'
    parameters = {
      'symbol': 'USD_JPY',
      'count': 10
    }
    self.private_authorization_get()
    res = requests.get(self.endpoint + self.path, headers=self.client.headers, params=parameters)
    return res.json()


  # private API methods(POST)
  def place_buy_order(self, size):
    method = 'POST'
    self.path = '/v1/order'
    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    reqBody = {
      "symbol": settings.tradeCurrency,
      "side": 'BUY',
      "size": str(size),
      "executionType": 'MARKET'
    }

    text = timestamp + method + self.path + json.dumps(reqBody)
    sign = hmac.new(bytes(settings.secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
    self.private_authorization_post(timestamp, sign)
    
    res = requests.post(self.endpoint + self.path, headers=self.client.headers, data=json.dumps(reqBody))
    return res.json()


  def place_sell_order(self, size):
    method = 'POST'
    self.path = '/v1/order'
    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    reqBody = {
      "symbol": settings.tradeCurrency,
      "side": 'SELL',
      "size": str(size),
      "executionType": 'MARKET'
    }

    text = timestamp + method + self.path + json.dumps(reqBody)
    sign = hmac.new(bytes(settings.secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
    self.private_authorization_post(timestamp, sign)

    res = requests.post(self.endpoint + self.path, headers=self.client.headers, data=json.dumps(reqBody))
    return res.json()

  def close_order(self, position_id: int, size: str):
      '''
      position_idを指定して決済する
      {
        "status": 0,
        "data": [
          {
            "rootOrderId": 123456789,
            "clientOrderId": "abc123",
            "orderId": 123456789,
            "symbol": "USD_JPY",
            "side": "BUY",
            "orderType": "NORMAL",
            "executionType": "LIMIT",
            "settleType": "CLOSE",
            "size": "10000",
            "price": "135.5",
            "status": "WAITING",
            "expiry": "20230418",
            "timestamp": "2019-03-19T01:07:24.467Z"
          }
        ],
        "responsetime": "2019-03-19T01:07:24.557Z"
      }
      '''
      method = 'POST'
      self.path = '/v1/closeOrder'
      timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
      reqBody = {
        "symbol": settings.tradeCurrency,
        "side": 'SELL',
        "executionType": 'MARKET',
        "settlePosition": [
            {
              "positionId": position_id,
              "size": size
            }
        ]
      }

      text = timestamp + method + self.path + json.dumps(reqBody)
      sign = hmac.new(bytes(settings.secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
      self.private_authorization_post(timestamp, sign)
      res = requests.post(self.endpoint + self.path, headers=self.client.headers, data=json.dumps(reqBody))
      return res.json()

  def close_out(self):
      # 全ての建玉を決済する
      pass


class Ticker(object):
  def __init__(self, time: datetime, bid: float, ask: float):
    self.time = time
    self.bid = bid
    self.ask = ask

  @property
  def mid_price(self):
    return (self.bid + self.ask) / 2

  @property
  def values(self):
    return {
      'time': self.time,
      'bid': self.bid,
      'ask': self.ask
    }

  def truncate_date_time(self, duration) -> datetime:
    ticker_time = self.time
    if duration == "1m":
      time_format = '%Y-%m-%d %H:%M'
    elif duration == '5m':
      new_minute = math.floor(self.time.minute / 5) * 5
      ticker_time = datetime(self.time.year, self.time.month, self.time.day, self.time.hour, new_minute)
      time_format = '%Y-%m-%d %H:%M'
    elif duration == '30m':
      new_minute = math.floor(self.time.minute / 30) * 30
      ticker_time = datetime(self.time.year, self.time.month, self.time.day, self.time.hour, new_minute)
      time_format = '%Y-%m-%d %H:%M'
    elif duration == '1h':
      time_format = '%Y-%m-%d %H'
    elif duration == '1s':
      time_format = '%Y-%m-%d %H:%M:%S'
    elif duration == '4h':
      new_hour = math.floor(self.time.hour / 4) * 4
      ticker_time = datetime(self.time.year, self.time.month, self.time.day, new_hour, 0)
      time_format = '%Y-%m-%d %H'

    else:
      logger.warning("Unknown duration: {0}".format(duration))

    str_date = datetime.strftime(ticker_time, time_format)
    return datetime.strptime(str_date, time_format)