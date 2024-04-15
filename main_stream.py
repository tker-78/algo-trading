import app.controllers.stream as stream
import logging
import schedule
import time

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    streamer = stream.Streamer()
    print("streaming tick data...")
    logger.info('action=stream starting...')
    # streamer.run()

    open_job = schedule.every().day.at("07:00", "Asia/Tokyo").do(streamer.run)

    while True:
        schedule.run_pending()
        time.sleep(1)