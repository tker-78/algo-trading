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
        try:
            while True:
                if cond.get_equity() < cond.initial_balance * 0.9:
                    logger.info(f'action=execute close_out started | {cond.values}')
                    cond.close_out()
                    logger.info(f'action=execute close_out finished | {cond.values}')
                    break

                logger.info(f'action=execute current conductor values | {cond.values}')
                cond.get_data(5) # should be modified because it is hardcoded
                print(cond.data.tail())

                # execute momentum simulation
                # 最初に建玉を持っているか確認する
                open_positions = cond.get_position()
                if len(open_positions["data"]["list"]) > 0:
                    cond.active_orders.append(open_positions["data"]["list"][0]["orderId"])
                    cond.units += int(open_positions["data"]["list"][0]["size"])
                    cond.position = 1

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

                time.sleep(5)
        except Exception as e:
            logger.error(f'action=execute error | {e}')

        finally:
            logger.info(f'action=execute exit | {cond.values}')

    def stream():
        streamer = Streamer()
        print("streaming tick data...")
        streamer.run()

    # tpe = ThreadPoolExecutor(max_workers=2)
    # tpe.submit(stream)

    # uncomment here if you want to run the execute function
    # tpe.submit(execute)
