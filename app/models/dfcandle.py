from app.models.candle import BaseCandleMixin
import numpy as np
from app.models.candle import factory_base_candle
from datetime import datetime


class DataframeCandle(object):
  """
  特定の期間のcandleを格納し、分析、表示に使うデータを準備、整形するためのクラス
  """

  def __init__(self, duration: str):
    self.duration = duration
    self.candle_cls = factory_base_candle(duration)
    self.candles = []

  def set_all_candles(self, limit: int = 100) -> list:
    self.candles = self.candle_cls.get_all_candles(limit=limit)
    return self.candles

  def set_candles_between(self, start_time: datetime, end_time: datetime) -> list:
    self.candles = self.candle_cls.get_candles_between(start_time, end_time)
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
