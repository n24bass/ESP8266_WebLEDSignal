このプログラムは前に書いた [NodeMCU で web LED signal](http://qiita.com/n24bass/items/bc96baaaad7359dca9bc) の MicroPython 版です。処理内容はほぼ同じで新たなリクエストがあると現在の処理をキャンセルします。点滅の間隔を直接タイマの設定値にしている点が異なります。元の Lua のコードは PWM もタイマ処理でしようかと考えていた名残りで無駄に何度もタイマ割込みをしていたのを止めました。

この MicroPython 実装では一旦ステーションモードでアクセスポイントに接続すると、その接続情報を記憶してリセット後にも自動的に接続を試行します。また、アクセスポイントモードでも動作しています。その辺は適当に制御が必要でしょう。

[YouTube](https://www.youtube.com/watch?v=48F32NLfHhA)の動画も更新しました。
