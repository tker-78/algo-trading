import websocket
import json
import logging
import datetime
from gmo.apiclient import Ticker
from app.models.candle import create_candle
from app.models.candle import UsdJpyBaseCandle1M
from gmo.apiclient import Ticker

logger = logging.getLogger(__name__)

class Streamer():
  def on_open(self, ws, option={}):
    message = {
      "command": "subscribe",
      "channel": "ticker",
      "symbol": "USD_JPY"
    }
    ws.send(json.dumps(message))

  def on_message(self, message, ws):
    data = json.loads(ws)
    # save to database
    # 受信形式 = ++Rcv raw: b'\x81o{"symbol":"USD_JPY","ask":"147.182","bid":"146.975","timestamp":"2024-03-08T23:58:40.157574Z","status":"CLOSE"}'

    # data["timestamp"]をdatetimeに変換する
    dateTime = datetime.datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

    # tickerオブジェクトを作成する
    ticker = Ticker(dateTime, data["bid"], data["ask"])

    # data["bid"], data["ask"]をfloatに変換してtickerに格納する
    ticker.ask = float(data["ask"])
    ticker.bid = float(data["bid"])
    

    is_created = create_candle(ticker)
    if is_created:
      print("candle created")
      print("symbol:", data["symbol"], "ask:", data["ask"], "bid:", data["bid"], "time:", data["timestamp"])
      print("ticker", ticker.values)








  def run(self):
    websocket.enableTrace(False)
    wsEndPoint = "wss://forex-api.coin.z.com/ws/public/v1"
    self.ws = websocket.WebSocketApp(wsEndPoint)
    self.ws.on_message = self.on_message
    self.ws.on_open = self.on_open
    self.ws.run_forever()
