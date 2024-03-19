from app.models.backtest import BackTestBase
import mplfinance as mpf
from matplotlib import pyplot as plt
import numpy as np

class BackTestLongOnly(BackTestBase):
  '''買いのみのバックテストクラス
  
  
  '''

  def perf_simulation(self):
    # 戦略のパフォーマンスをシミュレーションする
    # position columnの作成後に呼び出すこと
    self.data['strategy'] = self.data['position'].shift(1) * self.data['return']
    print(self.data[["return", "strategy"]].sum().apply(np.exp))
    self.data[["return", "strategy"]] = self.data[['return', 'strategy']].cumsum().apply(np.exp)
    plt.plot(self.data["return"], label="return")
    plt.plot(self.data["strategy"], label="strategy")
    plt.legend()
    plt.show()

  def run_sma_strategy(self, sma1, sma2, candle_plot=True, return_plot=False, positioning_plot=False):
    '''sma売買戦略
    長い方のsmaが短い方のsmaよりも上であれば、買いポジションをとる。
    '''
    msg = f'\n\nRunning sma strategy | sma1={sma1} & sma2={sma2}'
    msg += f'\nfixed costs {self.ftc} | '
    msg += f'\nproportional costs {self.ptc}'
    print(msg)
    print("=" * 55)
    self.position = 0 # ポジションを初期化する
    self.trades = 0 # まだトレードは実行していない
    self.amount = self.initial_amount
    self.data["sma1"] = self.data["close"].rolling(sma1).mean()
    self.data["sma2"] = self.data["close"].rolling(sma2).mean()

    # position列の作成
    self.data['position'] = np.where(self.data["sma1"] > self.data["sma2"], 1, -1)
    self.perf_simulation()



    # シグナルに基づく売買の実行
    for i in range(sma2, len(self.data)):
      if self.position == 0:
        if self.data["sma1"].iloc[i] > self.data["sma2"].iloc[i]:
          '''短期のsmaが長期のsmaを上回っているので、買いのモメンタムを表す
          '''
          self.place_buy_order(i)
          self.position = 1
      elif self.position == 1:
        if self.data["sma1"].iloc[i] < self.data["sma2"].iloc[i]:
          '''短期のsmaが長期のsmaを下回っているので、売りのモメンタムを表す
          '''
          self.place_sell_order(i)
          self.position = 0
          self.trades += 1
    self.close_out(i)

    # candleをプロットする
    if candle_plot:
        mpf.plot(self.data, type='candle', mav=[sma1, sma2])

    # 対数収益率をプロットする
    if return_plot:
        plt.hist(self.data["return"], bins=35)
        plt.show()

    # マーケットポジショニングをプロットする
    if positioning_plot:
        # todo: step(pulse)の実装方法が不明
        plt.hist(self.data["position"], bins=35)
        plt.show()

  def run_momentum_strategy(self, momentum):
    '''momentum戦略
    Parameters:
    ===========
    momentum: int
      number of days for mean return calculation
    ''' 
    msg = f'\n\nRunning momentum strategy | {momentum} days'
    msg += f'\nfixed costs {self.ftc} | '
    msg += f'\nproportional costs {self.ptc}'
    print(msg)
    print("=" * 55)
    self.position = 0 # ポジションを初期化する
    self.trades = 0 # まだトレードは実行していない
    self.amount = self.initial_amount
    self.data["momentum"] = self.data["return"].rolling(momentum).mean()
    self.data["position"] = np.where(self.data["return"].rolling(momentum).mean() > 0, 1, 0)
    self.perf_simulation()

    print(self.data)


    # シグナルに基づく売買の実行
    for i in range(momentum, len(self.data)):
      if self.position == 0:
        if self.data["momentum"].iloc[i] > 0:
          self.place_buy_order(i)
      elif self.position == 1:
        if self.data["momentum"].iloc[i] < 0:
          self.place_sell_order(i)
    self.close_out(i)






