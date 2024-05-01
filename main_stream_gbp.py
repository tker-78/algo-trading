import app.controllers.stream as stream
import logging
import schedule
import time
import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=settings.logFileNameStream, format='%(asctime)s - %(name)s - %(levelname)s -%(message)s')

if __name__ == '__main__':
    streamer_gbp = stream.Streamer("GBP_JPY")
    print(f"streaming tick data {streamer_gbp.currency}...")
    logger.info(f'action=stream starting... {streamer_gbp.currency}...')

    streamer_gbp.run()

    open_job2 = schedule.every().hour.at(":00", "Asia/Tokyo").do(streamer_gbp.run)


    while True:
        schedule.run_pending()
        time.sleep(1)