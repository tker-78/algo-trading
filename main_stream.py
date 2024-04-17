import app.controllers.stream as stream
import logging
import schedule
import datetime
import time
import sys
from app.models.conductor import Conductor

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # streamer = stream.Streamer()
    # print("streaming tick data...")
    # logger.info('action=stream starting...')
    # # streamer.run()
    open_job1 = schedule.every().day.at("23:44", "Asia/Tokyo").do(streamer.run)
    open_job2 = schedule.every().day.at("00:00", "Asia/Tokyo").do(streamer.run)

    while True:
        schedule.run_pending()
        time.sleep(1)







