# Match_Move

マッチムーブを実装しました


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


#記事
qiita:https://qiita.com/daikiclimate/private/01d878fc53c3485feb59
