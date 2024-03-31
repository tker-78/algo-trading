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
    endpoint = "https://forex-api.coin.z.com/public"
    path = '/v1/ticker'
    res = requests.get(endpoint + path)
    js = res.json()
    usd_jpy_ticker = js['data'][0]
    ask = float(usd_jpy_ticker['ask'])
    bid = float(usd_jpy_ticker['bid'])
    truncated = math.floor((ask - bid) * 1000 ) / 10
    return truncated



  # authorization
  def private_authorization_get(self):
    # todo
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
    self.path      = '/v1/account/assets'
    self.private_authorization_get()

    res = requests.get(self.endpoint + self.path, headers=self.client.headers)
    return res.json()

  def get_open_positions(self):
    '''
    response: 
    {
      "status": 0,
      "data": {
        "list": [
          {
            "positionId": 123456789,
            "symbol": "USD_JPY",
            "side": "BUY",
            "size": "10000",
            "orderedSize": "0",
            "price": "141.269",
            "lossGain": "-1980",
            "totalSwap":"0" ,
            "timestamp": "2019-03-21T05:18:09.011Z"
          }
        ]
      },
      "responsetime": "2019-03-19T02:15:06.095Z"
    }
    '''
    self.path = '/v1/openPositions'
    self.private_authorization_get()

    res = requests.get(self.endpoint + self.path, headers=self.client.headers)
    return res.json()

  def get_execution(self, order_id: str):
    '''
    response: {'status': 0, 'data': {'list': [{'amount': '0', 'executionId': 3368298, 'fee': '0', 'lossGain': '0', 'orderId': 4015908, 'positionId': 1640914, 'price': '151.365', 'settleType': 'OPEN', 'settledSwap': '0', 'side': 'BUY', 'size': '10000', 'symbol': 'USD_JPY', 'timestamp': '2024-03-29T08:21:25.985Z'}]}, 'responsetime': '2024-03-29T08:28:07.791Z'}
    '''
    self.path = '/v1/executions'
    self.private_authorization_get()
    params = {'orderId': str(order_id)}
    res = requests.get(self.endpoint + self.path, headers=self.client.headers, params=params )
    return res.json()

  def get_assets(self):
    self.path = '/v1/account/assets'
    self.private_authorization_get()
    res = requests.get(self.endpoint + self.path, headers=self.client.headers) 
    return res.json()


  # private API methods(POST)
  def place_buy_order(self, size):
    method = 'POST'
    self.path = '/v1/order'
    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    reqBody = {
      "symbol": 'USD_JPY',
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
      "symbol": 'USD_JPY',
      "side": 'SELL',
      "size": str(size),
      "executionType": 'MARKET'
    }

    text = timestamp + method + self.path + json.dumps(reqBody)
    sign = hmac.new(bytes(settings.secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
    self.private_authorization_post(timestamp, sign)

    res = requests.post(self.endpoint + self.path, headers=self.client.headers, data=json.dumps(reqBody))
    return res.json()

  def close_order(self, position_id: int, size: int):
      '''
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
        "symbol": 'USD_JPY',
        "side": 'SELL',
        "executionType": 'MARKET',
        "settlePosition": {
          "positionId": position_id,
          "size": size
        }
      }

      text = timestamp + method + self.path + json.dumps(reqBody)
      sign = hmac.new(bytes(settings.secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
      self.private_authorization_post(timestamp, sign)
      res = requests.post(self.endpoint + self.path, headers=self.client.headers, data=json.dumps(reqBody))
      return res.json()

  def close_out(self):
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