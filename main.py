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
from app.models.backtestlongonly import BackTestLongOnly
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

  # def run_strategies():
  #   lobt.run_sma_strategy(4,35,plot=True)

  lobt = BackTestLongOnly(
      # datetime(2022, 1,2, 17, 00), 
      # datetime(2022, 12, 30, 16, 58), 
      datetime(2021, 1, 4),
      datetime(2021, 12, 30),
      "1m", 
      100000, 
      0, 
      0,
      '2021'
    )
  print(type(lobt.data))

  lobt.run_momentum_strategy(500, False)

  # run_strategies()
