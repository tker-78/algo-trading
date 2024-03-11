import logging
import sys
import requests
import json
import hmac
import hashlib
import time
from datetime import datetime
import settings
from gmo.apiclient import APIPrivate
from app.controllers.stream import Streamer
from app.models.candle import UsdJpyBaseCandle1M


# class SampleClass(object):
#   @classmethod
#   def show(cls, args):
#     print(cls.__name__, args)


if __name__ == '__main__':

  apiClient = APIPrivate(settings.apiLabel, settings.apiKey, settings.secretKey)
  # print("Balance: {}".format(apiClient.get_balance()))
  # print("Open Positions: {}".format(apiClient.get_open_positions()))
  streamer = Streamer()
  streamer.run()
  # SampleClass.show("my name")


  # now1 = datetime(2020, 1,2,3,4,5)
  # # UsdJpyBaseCandle1M.create(now1, 1,2,3,4,5)
  # candle = UsdJpyBaseCandle1M.get(now1)
  # print(candle.time)
  # print(candle.open)
  # # candle.open = 1
  # candle.save()

