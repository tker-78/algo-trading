from contextlib import contextmanager
import logging
import threading

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session



logger = logging.getLogger(__name__)

Base = declarative_base()

# engine = create_engine(f'sqlite:///{settings.dbName}.sqlite?check_same_thread=False', pool_pre_ping=True)
engine = create_engine(f'postgresql+psycopg2://postgres:postgres@postgres_db_container/postgres_db', pool_pre_ping=True)
Session = scoped_session(sessionmaker(bind=engine))
lock = threading.Lock()



@contextmanager
def session_scope():
  session = Session()
  session.expire_on_commit = False
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
