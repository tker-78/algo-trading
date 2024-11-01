import websocket
from websocket._app import WebSocketApp
import json
import logging
import datetime
from gmo.apiclient import Ticker
from app.models.candle import create_candle
from gmo.apiclient import Ticker
import pytz
import constants
import settings

logger = logging.getLogger(__name__)

class Streamer():
  def __init__(self, currency):
    self.currency = currency
  def __init__(self, currency):
    self.currency = currency
  def on_open(self, ws, option={}):
    """
    This method is called when the websocket connection is established.

    Args:
        ws (WebSocketApp): The websocket app instance.
        option (dict, optional): Additional options for the websocket connection. Defaults to {}.

    Returns:
        None

    Raises:
        None

    Sends a subscription request to the websocket server for the specified symbol.
    """

    """
    This method is called when the websocket connection is established.

    Args:
        ws (WebSocketApp): The websocket app instance.
        option (dict, optional): Additional options for the websocket connection. Defaults to {}.

    Returns:
        None

    Raises:
        None

    Sends a subscription request to the websocket server for the specified symbol.
    """

    logging.info('action=websocket on_open starting...')
    message = {
      "command": "subscribe",
      "channel": "ticker",
      "symbol": self.currency 
      "symbol": self.currency 
    }
    ws.send(json.dumps(message))
    logging.info('action=websocket on_open finished.')

  def on_message(self, message, ws):
    """
    This method is called when a message is received from the websocket server.

    Args:
        message (str): The raw message received from the server.
        ws (WebSocketApp): The websocket app instance.

    Returns:
        None

    Raises:
        None

    Processes the received message, extracts the relevant data, and performs necessary actions.
    """
    """
    This method is called when a message is received from the websocket server.

    Args:
        message (str): The raw message received from the server.
        ws (WebSocketApp): The websocket app instance.

    Returns:
        None

    Raises:
        None

    Processes the received message, extracts the relevant data, and performs necessary actions.
    """
    data = json.loads(ws)
    # save to database
    # 受信形式 = ++Rcv raw: b'\x81o{"symbol":"USD_JPY","ask":"147.182","bid":"146.975","timestamp":"2024-03-08T23:58:40.157574Z","status":"CLOSE"}'

    # data["timestamp"]をdatetimeに変換する
    dateTime = datetime.datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Convert the datetime object to JST
    jst_dateTime = dateTime.astimezone(pytz.timezone('Asia/Tokyo'))
    # offset = datetime.timedelta(hours=9)
    # jst_dateTime = jst_dateTime + offset

    # tickerオブジェクトを作成する
    ticker = Ticker(jst_dateTime, data["bid"], data["ask"])

    # data["bid"], data["ask"]をfloatに変換してtickerに格納する
    ticker.ask = float(data["ask"])
    ticker.bid = float(data["bid"])

    for duration in constants.DURATIONS:
      create_candle(ticker, duration, self.currency)
      # if is_created:
      #   logger.info(f'action=on_message candle created | {duration} | {ticker.values}')
      #   print("{} candle created".format(duration))
      #   print("ticker", ticker.values)
      create_candle(ticker, duration, self.currency)
      # if is_created:
      #   logger.info(f'action=on_message candle created | {duration} | {ticker.values}')
      #   print("{} candle created".format(duration))
      #   print("ticker", ticker.values)

    if ticker.time.minute == 59:
    if ticker.time.minute == 59:
      self.ws.close()
      print(f'websocket closed | {ticker.time}')
      logger.info(f'action=on_message websocket closed at specified time | {ticker.time}')
      logger.info(f'action=on_message websocket closed at specified time | {ticker.time}')


  def run(self):

    """
    Starts the websocket connection and runs it forever.

    Args:
        self (Streamer): An instance of the Streamer class.

    Raises:
        Exception: If an error occurs during the websocket connection.

    Returns:
        None

    """

    """
    Starts the websocket connection and runs it forever.

    Args:
        self (Streamer): An instance of the Streamer class.

    Raises:
        Exception: If an error occurs during the websocket connection.

    Returns:
        None

    """
    print('websocket starting...')
    logging.info('action=websocket starting...')
    websocket.enableTrace(False)
    wsEndPoint = "wss://forex-api.coin.z.com/ws/public/v1"
    try:
      self.ws = websocket.WebSocketApp(wsEndPoint)
    except Exception as e:
      logger.info(f'error: {e}')

    try:
      self.ws.on_message = self.on_message
      print(self.ws.on_message)
      self.ws.on_open = self.on_open
      self.ws.run_forever()
    except Exception as e:
      logger.info(f'error: {e}')

    print("websocket finished.")
    logging.info('action=websocket finished.')

  def close(self):
    self.ws.close()
    print("websocket closed.")
