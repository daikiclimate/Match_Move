# Match_Move

マッチムーブを実装しました

元動画

![source](https://user-images.githubusercontent.com/40888763/87899006-c6edeb00-ca8a-11ea-80b3-574088a5804b.gif)


結果

![result](https://user-images.githubusercontent.com/40888763/87899036-e6851380-ca8a-11ea-9715-027b703578d4.gif)

ちょっと容量落とす際にちょっとずれてしまったけど、元々のmp4は同じものです

# 画像のマッチムーブ

```
python match_move.py images/base.png images/box.png images/ad.png 
```

第１引数
探索元の画像。

第２引数
探索したい特定領域の画像。スクショで良い
座標を指定するよりもこっちのが使い勝手いいかなと思った

第３引数
探索した特定領域を置き換える先の画像。差込広告のような感じ

第４引数
--output output/output.jpg

出力画像の名前を変更可能

第５引数
--param 1
特定領域の大きさが大きすぎる際に、うまく特徴点マッチングができない場合がある。

デフォルトでは１。5の場合は第２引数の画像を1/5のサイズに小さくする。
なるべく、探索元の画像内のやつを同じサイズの方がうまくいきやすい

# 動画のマッチムーブ

```
python video_process.py videos/sample.mp4 videos/box.jpg videos/ad.jpg 
```

第１引数
動画名。

第２引数
探索したい特定領域の画像。スクショで良い
座標を指定するよりもこっちのが使い勝手いいかなと思った

第３引数
探索した特定領域を置き換える先の画像。差込広告のような感じ

第４引数
--output_video
default "output.mp4"

出力動画の名前。基本はoutputディレクトリ内にこの名前で保存される

第５引数
--param
defalt 1

特定領域の大きさが大きすぎる際に、うまく特徴点マッチングができない場合がある。
デフォルトでは１。5の場合は第２引数の画像を1/5のサイズに小さくする。
なるべく、探索元の画像内のやつを同じサイズの方がうまくいきやすい

第6引数
--fix
default True

動画なので、ホモグラフィー変換をミスった時に1個前のフレームをコピーして修正することができる.

第7引数
--psnr_th
default 4

fixする際に、psnrで閾値以上の場合に修正を行う。画像によって、最低のpsnrが違うので、調整が必要




# 記事

qiita:https://qiita.com/daikiclimate/private/01d878fc53c3485feb59
