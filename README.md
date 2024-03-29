# algo trading with Python

Pythonを用いたアルゴリズムトレードアプリケーションを構築する。  

UdemyのPython+シストレの教材を参考に、GMOコインのFX APIを用いて
自動トレードを行う。

売買結果を保存するため、データベースとの連携も行う。
Dockerなどの仮想環境は構築しないことにする。

## 基本設計

streamは稼働し続ける。

指定したduration(デフォルトは4h)のスパンで、
データフレームを作成し、モメンタムの分析を行う。
シグナルが点灯したら、次のローソクのopenで購入する。  
トレードを監視するオブジェクトを作成してトレードの管理を行う。(TradeBaseクラス)






## タスクリスト
- [x] streamデータから4H足のキャンドルデータを保存する
- [ ] streamデータを使用してmomentumのリアルタイム判定を行う(売り買いのシグナルの発生)
    - streamデータが入ってきたら、pd.DataFrameに格納して、momentumを計算する
- [ ] 売買のAPIの実装
- [ ] 売買可能なスプレッド幅の判定
    - スプレッドが大きい時には取引をせず、スプレッドが収まるまで保留する
- [ ] クラウドへのデプロイ(安定稼働のため)