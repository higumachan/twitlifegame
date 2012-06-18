
flaskprojectのディレクトリにこのモジュールを配置する


まずsettings.pyに自分のキーを入れる
	key = "your cunsumar key"
	secret = "your cunsumar secret key"

appの最初に
from flask_twitter.TwitterPlugin import *
を書き

あとは、Twitterの認証の必要があるViewに
@twitter_login
を@app.routeの下に付け足すだけ
これを付けるViewには必ずapi=Noneという引数が必要
これによりViewの中でtweepy(https://github.com/tweepy/tweepy)のapiを使うことができる


コールバックになるViewには
@twitter_callback
を付けること
あと、コールバックのViewは必ず
flask.Responseを返すこと

TODO
 まだ、app.routeでしかテストしてない
 コールバックの制約がおおい
