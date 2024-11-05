import time
import logging
import settings
from app.models.conductor import Conductor
from app.models.candle import factory_base_candle
import constants
from app.models.candle import factory_base_candle
from logging.handlers import RotatingFileHandler


logging.basicConfig(level=logging.INFO, filename=settings.logFileName, format='%(asctime)s - %(name)s - %(levelname)s -%(message)s')
logger = logging.getLogger(__name__)

handler = RotatingFileHandler(settings.logFileName, maxBytes=10 * 1024, backupCount=10)

if __name__ == '__main__':

    # 監視用のオブジェクトの生成
    cond = Conductor()

    def delete_invalid_candles():
        for duration in constants.DURATIONS:
            logger.info(f"delete invalid candles... {settings.tradeCurrency}_{duration}")
            cls = factory_base_candle(settings.tradeCurrency, duration)
            cls.delete_invalid_candles()
        logger.info(f"delete invalid candles finished")

    def trade_rules_and_execution_long(last_momentum, latest_momentum):
        if last_momentum > constants.BUY_MOMENTUM_LOWER_LONG and cond.position == 0 and cond.check_spread():
            # スプレッドの制限が必要であれば、cond.check_spread()を購入条件に追加する
            logger.info(f'action=execute place buy order | {cond.values}')
            is_ok = cond.place_buy_order()
            if is_ok:
                logger.info(f'action=execute place buy order successful')
            else:
                logger.info(f'action=execute place buy order failed')
        elif last_momentum < constants.SELL_MOMENTUM_LONG and cond.position == 1:
            is_ok = cond.close_position("SELL")
            if is_ok:
                logger.info(f'action=execute place sell order successful')
            else:
                logger.info(f'action=execute place sell order failed')
        elif latest_momentum < constants.LOSSCUT_MOMENTUM_LONG and cond.position == 1:
            is_ok = cond.close_position("SELL")
            if is_ok:
                logger.info(f'action=execute losscut executed.')
                # ロスカットした場合は、一定時間取引を凍結する。
                logger.info(f'snoozing the trade for {cond.duration}')
                time.sleep(constants.LOSS_CUT_SLEEP_TIME[cond.duration])
            else:
                logger.info(f'action=execute losscut failed.')
    
    def trade_rules_and_execution_short(last_momentum, latest_momentum):
        if last_momentum < constants.SELL_MOMENTUM_UPPER_SHORT and cond.position == 0 and cond.check_spread():
            logger.info(f'action=execute place sell order | {cond.values}')
            is_ok = cond.place_sell_order()
            if is_ok:
                logger.info(f'action=execute place sell order successful')
            else:
                logger.info(f'action=execute place sell order failed')
        elif last_momentum > constants.BUY_MOMENTUM_SHORT and cond.position == 1:
            is_ok = cond.close_position("BUY")
            if is_ok:
                logger.info(f'action=execute place buy order successful')
            else:
                logger.info(f'action=execute place buy order failed')
        elif latest_momentum > constants.LOSSCUT_MOMENTUM_SHORT and cond.position == 1:
            is_ok = cond.close_position("BUY")
            if is_ok:
                logger.info(f'action=execute losscut executed.')
                logger.info(f'snoozing the trade for {cond.duration}')
                time.sleep(constants.LOSS_CUT_SLEEP_TIME[cond.duration])
            else:
                logger.info(f'action=execute losscut failed.')

        


    # 実行すると実際に約定するので注意!
    def execute():
        # 取引時間外のデータをデータベースから削除する
        delete_invalid_candles()


        # 起動時に建玉を持っていれば、それをcondに反映する
        # positionIdを使用する
        logger.info("getting current position...")
        try:
            cond.get_open_position()
        except Exception as e:
            logger.info(f'error: {e}')

        logger.info(f'cond.values: {cond.values}')

        while True:
            # momentumを指定してデータを生成する
            cond.get_data(int(settings.tradeMomentum))
            logger.info(f'cond.values: {cond.values}')
            logger.info(cond.data.tail(6))
            print(cond.data.tail(6))

            # 手動で決済した場合に、condに反映する
            open_positions = cond.api_client.get_open_positions()
            try:
                if len(open_positions["data"]["list"]) == 0:
                    cond.active_orders = []
                    cond.units = 0
                    cond.position = 0
            except Exception as e:
                logger.info(f'error: {e}')

            # シミュレーションを実行する
            logger.info(f'action=execute start checking to place orders | {cond.values} ')
            last_momentum = cond.data["momentum"].iloc[-2]
            latest_momentum = cond.data["momentum"].iloc[-1]
            print(f"length of data:{len(cond.data)}")
            
            # トレードを実行する関数(実行する場合はアンコメント)
            if len(cond.data) > int(settings.tradeMomentum) + 1:
                trade_rules_and_execution_long(last_momentum, latest_momentum)

            # trade duration毎に設定した秒数待機する
            time.sleep(constants.SLEEP_TIME[cond.duration])

    # uncomment here if you want to run the automatic trading
    try:
        execute()
    except Exception as e:
        print(f'error: {e}')

