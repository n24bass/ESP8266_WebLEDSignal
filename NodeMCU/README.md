infinite loop さんが Crystal Signal Pi と言う製品を発売されました。Raspberry Pi を使った RGB color LED 信号灯です。根が貧乏性なワタシは、NodeMCU で間に合うよね、と思い試してみました。当初は MicroPython で考えてみたものの、socket の非同期動作ができないと言うことで不慣れな Lua で書いています。結局 socket の非同期処理とは関係なく、コマンドのパラメータをグローバルに置いてタイマで LED の点滅制御をしています。排他、それ何？みたいな雑なコードですみません。無駄に 100ms 毎にタイマ割込みを入れているのは PWM による LED の明るさ制御も自前でやってみようとした名残りです。

http://example.com//ctrl/?red=0&green=64&blue=255&period=500&rpt=300 のようににして使います。YouTubeにバラックで動作中の様子を置きました。
