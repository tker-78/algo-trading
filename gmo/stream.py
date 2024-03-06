import websocket
import json

class Streamer():
  def on_open(self, ws, option={}):
    message = {
      "command": "subscribe",
      "channel": "ticker",
      "symbol": "USD_JPY"
    }
    ws.send(json.dumps(message))

  def on_message(self,message, ws, option={}):
    print(message)


  def run(self):
    websocket.enableTrace(True)
    wsEndPoint = "wss://forex-api.coin.z.com/ws/public/v1"
    self.ws = websocket.WebSocketApp(wsEndPoint)
    self.ws.on_message = self.on_message
    self.ws.on_open = self.on_open
    self.ws.run_forever()
