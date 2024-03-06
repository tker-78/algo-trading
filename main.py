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
from gmo.stream import Streamer


if __name__ == '__main__':

  apiClient = APIPrivate(settings.apiLabel, settings.apiKey, settings.secretKey)
  print("Balance: {}".format(apiClient.get_balance()))
  print("Open Positions: {}".format(apiClient.get_open_positions()))
  streamer = Streamer()
  streamer.run()
