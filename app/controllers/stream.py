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

logger = logging.getLogger(__name__)

class Streamer():
  def on_open(self, ws, option={}):
    logging.info('action=websocket on_open starting...')
    message = {
      "command": "subscribe",
      "channel": "ticker",
      "symbol": "USD_JPY"
    }
    ws.send(json.dumps(message))
    logging.info('action=websocket on_open finished.')

  def on_message(self, message, ws):
    data = json.loads(ws)
    # save to database
    # 受信形式 = ++Rcv raw: b'\x81o{"symbol":"USD_JPY","ask":"147.182","bid":"146.975","timestamp":"2024-03-08T23:58:40.157574Z","status":"CLOSE"}'

    # data["timestamp"]をdatetimeに変換する
    dateTime = datetime.datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Convert the datetime object to JST
    jst_dateTime = dateTime.astimezone(pytz.timezone('Asia/Tokyo'))
    offset = datetime.timedelta(hours=9)
    jst_dateTime = jst_dateTime + offset

    # tickerオブジェクトを作成する
    ticker = Ticker(jst_dateTime, data["bid"], data["ask"])

    # data["bid"], data["ask"]をfloatに変換してtickerに格納する
    ticker.ask = float(data["ask"])
    ticker.bid = float(data["bid"])

    for duration in constants.DURATIONS:
      is_created = create_candle(ticker, duration)
      if is_created:
        logger.info(f'action=on_message candle created | {duration} | {ticker.values}')
        print("{} candle created".format(duration))
        print("ticker", ticker.values)


  def run(self):
    print('websocket starting...')
    logging.info('action=websocket starting...')
    websocket.enableTrace(False)
    wsEndPoint = "wss://forex-api.coin.z.com/ws/public/v1"
<<<<<<< HEAD
    self.ws = WebSocketApp(wsEndPoint)
    self.ws.on_message = self.on_message
    self.ws.on_open = self.on_open
    self.ws.run_forever()
=======
    try:
      self.ws = websocket.WebSocketApp(wsEndPoint)
    except Exception as e:
      logger.info(f'error: {e}')

    logger.info(f'ws: {self.ws}')

    try:
      self.ws.on_message = self.on_message
      self.ws.on_open = self.on_open
      self.ws.run_forever()
    except Exception as e:
      logger.info(f'error: {e}')

    print("websocket finished.")
    logging.info('action=websocket finished.')
>>>>>>> 18845007eb578506aa8fc96e0f77e6f85597341c
