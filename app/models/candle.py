from contextlib import contextmanager
import logging
import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import desc
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base
from app.models.base import session_scope

import settings
from gmo.apiclient import Ticker

logger = logging.getLogger(__name__)

class BaseCandleMixin(object):
  time = Column(DateTime, primary_key=True, nullable=False)
  open = Column(Float)
  high = Column(Float)
  low = Column(Float)
  close = Column(Float)
  volume = Column(Integer)

  @classmethod
  def create(cls, time, open, close, high, low, volume):
    candle = cls(time=time, open=open, close=close, high=high, low=low, volume=volume)
    try:
      with session_scope() as session:
          session.add(candle)
          return True
    except IntegrityError:
      return False

  @classmethod
  def get(cls, time: datetime):
    with session_scope() as session:
      candle = session.query(cls).filter(cls.time == time).first()
    if candle is None:
      return None
    return candle
  
  def save(self):
    with session_scope() as session:
      session.add(self)

  @classmethod
  def get_all_candles(cls, limit=100):
    with session_scope() as session:
      candles = session.query(cls).all()
    
    if candles is None:
      return None
    
    return candles

  @classmethod
  def get_candles_between(cls, start_time: datetime, end_time: datetime):
    with session_scope() as session:
      candles = session.query(cls).filter(cls.time >= start_time).filter(cls.time <= end_time).all()
    
    if candles is None:
      return None
    
    return candles

  @classmethod
  def delete_invalid_candles(cls):
    print('delete invalid candles...')
    now = datetime.datetime.now()
    current_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    date_diff_from_saturday = (current_date.weekday() + 2) % 7
    date_diff_from_monday = date_diff_from_saturday - 2 
    start_time = current_date - datetime.timedelta(days=date_diff_from_saturday) + datetime.timedelta(hours=6)
    end_time = current_date - datetime.timedelta(days=date_diff_from_monday) + datetime.timedelta(hours=7)
    print(f'start_time: {start_time}, end_time: {end_time}')

    with session_scope() as session:
      candles = session.query(cls).filter(cls.time >= start_time).filter(cls.time < end_time).all()

    if candles is None:
      return None
    
    for candle in candles:
      print(candle.value)
      session.delete(candle)
      session.commit()

    print('finished delete invalid candles.')

  @property
  def value(self):
    return {
      'time': datetime.datetime.strftime(self.time, '%Y-%m-%d %H:%M:%S'),
      'open': self.open,
      'high': self.high,
      'low': self.low,
      'close': self.close
    }
class UsdJpyBaseCandle4H(BaseCandleMixin, Base):
  __tablename__ = 'USD_JPY_4H'

class UsdJpyBaseCandle1H(BaseCandleMixin, Base):
  __tablename__ = 'USD_JPY_1H'

class UsdJpyBaseCandle5M(BaseCandleMixin, Base):
  __tablename__ = 'USD_JPY_5M'

class UsdJpyBaseCandle1M(BaseCandleMixin, Base):
  __tablename__ = 'USD_JPY_1M'

class UsdJpyBaseCandle1s(BaseCandleMixin, Base):
  __tablename__ = 'USD_JPY_1S'

def factory_base_candle(duration) -> BaseCandleMixin:
  if duration == '4h':
    return UsdJpyBaseCandle4H
  elif duration == '1h':
    return UsdJpyBaseCandle1H
  elif duration == '1m':
    return UsdJpyBaseCandle1M
  elif duration == '5m':
    return UsdJpyBaseCandle5M
  elif duration == '1s':
    return UsdJpyBaseCandle1s
  else:
    return None

def create_candle(ticker: Ticker, duration) -> bool:
  cls = factory_base_candle(duration)
  ticker_time = ticker.truncate_date_time(duration)
  current_candle = cls.get(ticker_time)
  price = ticker.mid_price
  if current_candle is None:
    cls.create(ticker_time, price, price, price, price, 0)
    return True

  if current_candle.high < price:
    current_candle.high = price
  elif current_candle.low > price:
    current_candle.low = price
  current_candle.close = price
  current_candle.save()
  return False