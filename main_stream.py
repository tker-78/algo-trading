import app.controllers.stream as stream
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    streamer = stream.Streamer()
    print("streaming tick data...")
    logger.info('action=stream starting...')
    streamer.run()
    logger.info('action=stream finished.')
    print('streaming finished.')