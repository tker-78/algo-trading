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
- [ ] long-term trendingを使って、short-termでのトレードルールを切り替える
- [ ] logデータを配信するサーバー機能を設置する


## 使い方
mainスクリプトを`main.py`, `main_stream.py`の２つに分けている。
main.pyは自動売買の実行を、main_stream.pyはstreamデータの受信と保管を担当している。
Dockerを使って環境構築を行う。


## Dockerでの環境構築

Dockerイメージをlocalでビルドして、クラウドから利用する。






マルチプラットフォームのビルド
```bash
$ docker buildx build --platform=linux/amd64,linux/arm64 .
$ docker tag fcdc13304493 kktak02/algo-trading-trading:latest
$ docker push kktak02/algo-trading-trading:test
```

```bash
$ docker pull kktak02/algo-trading-trading:latest
```

```bash
$ docker compose up -d
$ docker compose exec -d trading python3 main_trading.py
```

実行中のトレードのログ確認
```bash
$ tail -f trading.log
```

トレードを強制終了
```bash
$ docker compose stop trading
```


## 使いにくい点
- SSH接続をしないと稼働状況が確認できない -> webアプリケーションとして公開する。(認証の実装はマスト)
- 単純に投資成績が悪い -> 徹底的にバックテストを行う。
- スプレッドが大きすぎて投資成績に悪影響 -> OANDAなど他のブローカーを採用する
- メモリの使用量が大きすぎて、たまにプログラムがフリーズする -> メモリを消費している原因を探る
- tmuxで複数の環境を作成するため、dropletの再起動の際の再設定に手間がかかる -> tmuxでの環境生成と実行を自動化する
- トレード通貨を切り替える際、mainプログラムを実行するまで現在のmomentumがわからない。 -> トレード中以外の通貨も含めてバックテストデータを蓄積して、webアプリケーションから参照できるようにする。



