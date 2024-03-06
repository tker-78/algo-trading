import requests
import settings
import hashlib
import hmac
from datetime import datetime
import time

class APIPrivate(object):
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



  def private_authorization(self):
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



  def get_balance(self):
    self.path      = '/v1/account/assets'
    self.private_authorization()

    res = requests.get(self.endpoint + self.path, headers=self.client.headers)
    return res.json()

  def get_open_positions(self):
    self.path = '/v1/openPositions'
    self.private_authorization()

    res = requests.get(self.endpoint + self.path, headers=self.client.headers)
    return res.json()