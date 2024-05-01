import app.controllers.stream as stream
import logging
import schedule
import time
import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=settings.logFileNameStream, format='%(asctime)s - %(name)s - %(levelname)s -%(message)s')

if __name__ == '__main__':
    streamer_usd = stream.Streamer("USD_JPY")
    print(f"streaming tick data {streamer_usd.currency}...")
    logger.info(f'action=stream starting... {streamer_usd.currency}...')

    streamer_usd.run()


    open_job1 = schedule.every().hour.at(":01", "Asia/Tokyo").do(streamer_usd.run)


    while True:
        schedule.run_pending()
        time.sleep(1)