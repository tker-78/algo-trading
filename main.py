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
      datetime(2022, 3,1), 
      datetime(2024, 3, 31), 
      "1m", 
      100000, 
      0, 
      0,
      '2022-03-25.csv'
    )

  lobt.run_momentum_strategy(3)

  # run_strategies()
