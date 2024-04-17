import time
import logging
import pandas as pd
import settings
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from gmo.apiclient import APIPrivate
from app.controllers.stream import Streamer
from app.models.conductor import Conductor
from app.models.candle import factory_base_candle
import constants
from app.models.candle import UsdJpyBaseCandle1M
from app.models.candle import factory_base_candle


# class SampleClass(object):
#   @classmethod
#   def show(cls, args):
#     print(cls.__name__, args)

logging.basicConfig(level=logging.INFO, filename=settings.logFileName, format='%(asctime)s - %(name)s - %(levelname)s -%(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    # 監視用のオブジェクトの生成
    cond = Conductor()

    # 実行すると実際に約定するので注意!
    def execute():

        # 取引時間外のデータをデータベースから削除する
        for duration in constants.DURATIONS:
            print('delete invalid candles...')
            logger.info(f'delete invalid candles... {duration}')
            cls = factory_base_candle(duration)
            cls.delete_invalid_candles()
        print('delete invalid candles finished.')
        logger.info('delete invalid candles finished.')


        # 起動時に建玉を持っていれば、それをcondに反映する
        # positionIdを使用する
        print("get position")
        logger.info("get position")
        try:
            cond.get_open_position()
        except Exception as e:
            print(f'error: {e}')
            logger.info(f'error: {e}')

        while True:
            # 自動トレード終了の条件を指定
            if cond.get_equity() < cond.initial_balance * 0.9:
                print(f'action=execute close_out started | {cond.values}')
                logger.info(f'action=execute close_out started | {cond.values}')
                cond.close_out()
                print(f'action=execute close_out finished | {cond.values}')
                logger.info(f'action=execute close_out finished | {cond.values}')
                break

            print(f'action=execute current conductor values | {cond.values}')
            logger.info(f'action=execute current conductor values | {cond.values}')
            cond.get_data(5) # should be modified because it is hardcoded
            print(cond.data.tail())

            # execute momentum simulation

            # 手動で決済した場合に、condに反映する
            if len(cond.api_client.get_open_positions()["data"]["list"]) == 0:
                cond.active_orders = []
                cond.units = 0
                cond.position = 0

            # シミュレーションを実行する
            logger.info(f'action=execute start checking to place orders | {cond.values} ')
            latest_momentum = cond.data["momentum"].iloc[-1]

            if latest_momentum > 0 and cond.position == 0 and cond.check_spread():
                logger.info(f'action=execute place buy order | {cond.values}')
                is_ok = cond.place_buy_order()
                if is_ok:
                    logger.info(f'action=execute place buy order successful')
                else:
                    logger.info(f'action=execute place buy order failed')
            elif latest_momentum < 0 and cond.position == 1 and cond.check_spread():
                is_ok = cond.close_position()
                if is_ok:
                    logger.info(f'action=execute place sell order successful')
                else:
                    logger.info(f'action=execute place sell order failed')

            time.sleep(constants.SLEEP_TIME[settings.tradeDuration])


    def stream():
        streamer = Streamer()
        print("streaming tick data...")
        streamer.run()

    # tpe = ThreadPoolExecutor(max_workers=2)
    # tpe.submit(stream)

    # uncomment here if you want to run the execute function
    # tpe.submit(execute)






