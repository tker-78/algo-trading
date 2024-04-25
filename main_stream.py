import app.controllers.stream as stream
import logging
import schedule
import time
import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=settings.logFileNameStream, format='%(asctime)s - %(name)s - %(levelname)s -%(message)s')

if __name__ == '__main__':
    streamer = stream.Streamer()
    print("streaming tick data...")
    logger.info('action=stream starting...')

    streamer.run()

    # open_job = schedule.every().day.at("07:00", "Asia/Tokyo").do(streamer.run)
    open_job = schedule.every().hour.at(":00", "Asia/Tokyo").do(streamer.run)


    while True:
        schedule.run_pending()
        time.sleep(1)