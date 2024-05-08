import os


DURATIONS = ["4h","1h", "30m", "1m", "5m"]

SLEEP_TIME = {"4h": 60, "1h": 30, "30m": 15, "1m": 5, "5m": 15}

LOSS_CUT_SLEEP_TIME = {"4h": 4 * 60 * 60, "1h": 60 * 60, "30m": 30 * 60, "5m": 5 * 60, "1m": 60}

ALLOWED_SPREAD = 7.0

# BUY_MOMENTUM_LOWER = 2 / 10**6 
BUY_MOMENTUM_LOWER = 0

BUY_MOMENTUM_UPPER = 50 / 10**6

SELL_MOMENTUM = 0

LOSSCUT_MOMENTUM = -400 / 10**6


ROOT_PATH = os.path.dirname(__file__)
