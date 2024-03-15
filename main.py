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
from app.models.backtest import BackTestBase
import constants

# class SampleClass(object):
#   @classmethod
#   def show(cls, args):
#     print(cls.__name__, args)


if __name__ == '__main__':

  # apiClient = APIPrivate(settings.apiLabel, settings.apiKey, settings.secretKey)

  # Since streamer is public API, apiClient authentication not required
  # streamer = Streamer()
  # streamer.run()

  df = BackTestBase(datetime(2023, 1, 1, 1, 1), datetime.now(), "1h", 100, 0, 0)

  df.get_data_from_csv("2022-03-25.csv")
  print(df.data)
  print(df.data.info())
  df.plot_data()