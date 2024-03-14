from app.models.candle import BaseCandleMixin
import talib
import numpy as np
from app.models.candle import factory_base_candle

# インジケータ類はコンポジションでdataframeが保持する
class Sma(object):
  def __init__(self, period: int, values: list):
    self.period = period
    self.values = values

class Ema(object):
  def __init__(self, period: int, values: list):
    self.period = period
    self.values = values



class DataframeCandle(object):
  """
  特定の期間のcandleを格納し、分析、表示に使うデータを準備、整形するためのクラス
  """

  def __init__(self, duration: str):
    self.duration = duration
    self.candle_cls = factory_base_candle(duration)
    self.candles = []
    self.smas = []
    self.emas = []


  def set_all_candles(self, limit: int = 100) -> list:
    self.candles = self.candle_cls.get_all_candles(limit=limit)
    return self.candles

  @property
  def opens(self) -> list:
    opens = []
    for candle in self.candles:
      opens.append(candle.open)
    return opens

  @property
  def highs(self) -> list:
    highs = []
    for candle in self.candles:
      highs.append(candle.open)
    return highs 

  @property
  def lows(self) -> list:
    lows = []
    for candle in self.candles:
      lows.append(candle.open)
    return lows

  @property
  def closes(self) -> list:
    closes = []
    for candle in self.candles:
      closes.append(candle.open)
    return closes 

  def add_sma(self, period: int):
    sma = Sma(period=period, values=talib.SMA(np.asarray(self.closes), timeperiod=period))
    self.smas.append(sma)

  def add_ema(self, period: int):
    ema = Ema(period=period, values=talib.EMA(np.asarray(self.closes), timeperiod=period))
    self.emas.append(ema)


  