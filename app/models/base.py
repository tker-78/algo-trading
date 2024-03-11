from contextlib import contextmanager
import logging
import threading

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import settings


logger = logging.getLogger(__name__)

Base = declarative_base()

engine = create_engine(f'sqlite:///{settings.dbName}.sqlite?check_same_thread=False')
Session = scoped_session(sessionmaker(bind=engine))
lock = threading.Lock()



@contextmanager
def session_scope():
  session = Session()
  session.ezpire_on_commit = False
  try:
    lock.acquire()
    yield session
    session.commit()
  except Exception as e:
    logger.error(f'action=session_scope error={e}')
    session.rollback()
    raise
  finally:
    lock.release()


def init_db():
  import app.models.candle
  Base.metadata.create_all(bind=engine)