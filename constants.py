import os


DURATIONS = ["4h","1h", "1m", "5m"]

SLEEP_TIME = {"4h": 60, "1h": 30, "1m": 5, "5m": 15}

ALLOWED_SPREAD = 5.0

BUY_MOMENTUM_LOWER = 5 / 100000

BUY_MOMENTUM_UPPER = 20 / 100000

SELL_MOMENTUM = 0


ROOT_PATH = os.path.dirname(__file__)
