import logging
import pandas as pd
import sys
import requests
import json
import hmac
import hashlib
import time
import matplotlib
import mplfinance as mpf
from datetime import datetime
import settings
from gmo.apiclient import APIPrivate
from app.controllers.stream import Streamer
from app.models.candle import UsdJpyBaseCandle1M
from app.models.dfcandle import DataframeCandle


# class SampleClass(object):
#   @classmethod
#   def show(cls, args):
#     print(cls.__name__, args)


if __name__ == '__main__':

  # apiClient = APIPrivate(settings.apiLabel, settings.apiKey, settings.secretKey)
  streamer = Streamer()
  streamer.run()

  # df = DataframeCandle(duration='1m', candle_cls=UsdJpyBaseCandle1M)
  # df.set_all_candles(limit=100)

