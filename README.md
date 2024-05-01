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
トレードを監視するオブジェクトを作成してトレードの管理を行う。(Conductorクラス)




## タスクリスト
- [x] streamデータから4H足のキャンドルデータを保存する
- [x] streamデータを使用してmomentumのリアルタイム判定を行う(売り買いのシグナルの発生)
    - streamデータが入ってきたら、pd.DataFrameに格納して、momentumを計算する
- [x] 売買のAPIの実装
- [x] 売買可能なスプレッド幅の判定
    - スプレッドが大きい時には取引をせず、スプレッドが収まるまで保留する
- [x] クラウドへのデプロイ(安定稼働のため)
    - [x] sshでアクセスして、遠隔でトレードの実行、中断の操作をできるようにする(digital oceanを使うなど。 )
- [ ] 暴落時の緊急決済を実装する
- [ ] midではなく、ask, bidの値で判定する
- [x] プログラム実行時に、positionの有無を確認する
- [ ] loggingの実装を整理する
- [x] 取引時間外のデータを削除する
- [ ] 適切な例外処理を行う
- [x] 取引時間外はプログラムの実行を停止またはスリープするようにスケジューリングする
- [ ] main.pyの不測の停止時に再起動できるようにする
- [ ] ask, bidのデータを格納するデータベースを作成する


