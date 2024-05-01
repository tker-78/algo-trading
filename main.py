import time
import logging
import settings
from app.models.conductor import Conductor
from app.models.candle import factory_base_candle
import constants
from app.models.candle import UsdJpyBaseCandle1M
from app.models.candle import factory_base_candle


logging.basicConfig(level=logging.INFO, filename=settings.logFileName, format='%(asctime)s - %(name)s - %(levelname)s -%(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    # 監視用のオブジェクトの生成
    cond = Conductor()

    # 実行すると実際に約定するので注意!
    def execute():

        # 取引時間外のデータをデータベースから削除する
        for duration in constants.DURATIONS:
            print(f'delete invalid candles... {settings.tradeCurrency}_{duration}')
            logger.info(f'delete invalid candles... {settings.tradeCurrency}_{duration}')
            cls = factory_base_candle(settings.tradeCurrency, duration)
            cls.delete_invalid_candles()
        print('delete invalid candles finished.')
        logger.info('delete invalid candles finished.')


        # 起動時に建玉を持っていれば、それをcondに反映する
        # positionIdを使用する
        print("getting current position...")
        logger.info("getting current position...")
        try:
            cond.get_open_position()
        except Exception as e:
            print(f'error: {e}')
            logger.info(f'error: {e}')

        print(f'cond.values: {cond.values}')
        logger.info(f'cond.values: {cond.values}')

        while True:
            # 自動トレード終了の条件を指定
            # try: 
            #     equity = cond.get_equity()
            #     if equity < cond.initial_balance * 0.8:
            #         print(f'action=execute close_out started') 
            #         logger.info(f'action=execute close_out started')

            #         cond.close_out()

            #         print(f'action=execute close_out finished')
            #         logger.info(f'action=execute close_out finished')

            #         break
            # except Exception as e:
            #     print(f'error: {e}')
            #     logger.info(f'error: {e}')

            # momentumを指定してデータを生成する
            cond.get_data(int(settings.tradeMomentum))

            print(f'cond.values: {cond.values}')
            logger.info(f'cond.values: {cond.values}')

            print(cond.data.tail(6))
            logger.info(cond.data.tail(6))


            # 手動で決済した場合に、condに反映する
            open_positions = cond.api_client.get_open_positions()
            try:
                if len(open_positions["data"]["list"]) == 0:
                    cond.active_orders = []
                    cond.units = 0
                    cond.position = 0
            except Exception as e:
                print(f'error: {e}')
                logger.info(f'error: {e}')


            # シミュレーションを実行する
            logger.info(f'action=execute start checking to place orders | {cond.values} ')
            latest_momentum = cond.data["momentum"].iloc[-1]

            if latest_momentum > constants.BUY_MOMENTUM_LOWER and latest_momentum < constants.BUY_MOMENTUM_UPPER and cond.position == 0:
                # スプレッドの制限が必要であれば、cond.check_spread()を購入条件に追加する
                logger.info(f'action=execute place buy order | {cond.values}')
                is_ok = cond.place_buy_order()
                if is_ok:
                    logger.info(f'action=execute place buy order successful')
                else:
                    logger.info(f'action=execute place buy order failed')
            elif latest_momentum < constants.SELL_MOMENTUM and cond.position == 1:
                is_ok = cond.close_position()
                if is_ok:
                    logger.info(f'action=execute place sell order successful')
                else:
                    logger.info(f'action=execute place sell order failed')

            time.sleep(constants.SLEEP_TIME[settings.tradeDuration])



    # uncomment here if you want to run the automatic trading
    execute()

