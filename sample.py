from app.models.conductor import Conductor
import time

if __name__ == '__main__':
    cond = Conductor()

    cond.place_sell_order()

    time.sleep(2)

    cond.close_position("BUY")