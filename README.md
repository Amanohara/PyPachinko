
# ぱちんこ遊技機プログラム

 ぱちんこ遊技機のプログラムをPythonで書いてみたものです。  
 発展途上なので、気付いたことがあれば**Issues**とかに書いていただけると助かります。  
 GPL v3.0で配布します。

## 環境
 Python3.9で書いています。  
 `Pandas`さえあれば動くはずです

## できること
 + 適当に10,000回くらい回したときの当たり具合やハマり具合を見れる
 + フォーマット通りに機種情報プログラムを組めば色々なスペックでシミュレーションできる

## 今後やりたいこと
 + 収支計算（ベースとかも組み込み、収支を計算する。グラフも書く）
 + 遊タイム(<s>面倒くさい</s>)
 + 電サポ回数の振り分け

## 仕組み
 各スペック機のベースとなるプログラムに、任意の機種情報を`import`させることで動きます。

 現在作成しているスペックは以下の通りです。

+ 確変ループ機 `kakuhen_roop.py`  
ex.冬のソナタ、海物語など
+ V-ST機(V確変ST機) `v-st.py`  
ex.聖戦士ダンバインなど
+ 1種2種混合機 `1+2mix.py`  
ex.戦姫絶唱シンフォギア、大工の源さんなど
+ **＜未実装＞**  転落抽せん機 `tenarku.py`  
ex.聖闘士星矢4など

たとえば、CRF戦姫絶唱シンフォギアっぽいスペックで試行するには、

`1+2mix.py`を開いて、  

```python
import random
import pandas as pd
import sys
from machine import symphogear as machine
```

と記載・加筆し、

```python
python 1+2mix.py <試行回数>
```
とすれば動きます。  
結果は`result.csv`に出力されます。

# 機種フォーマットの書き方

ベースとなるスペックで若干異なりますが、だいたい以下の通りです

## 必要な関数
動かすには、`imfomation`, `furiwake_heso`, `furiwake_denchu`, `migiuchi_judge`関数を作成します。

### imfomation
 各機種の情報です。当せん分母などを指定します。  
 たとえば、V-ST機だと 
```python
def information():
    # 特図1での大当たり確率[1/n]
    normal = 319.7
    # 特図2での大当たり確率[1/n]
    koukaku = 32.4
    # 特図1当せん時の電サポ回数[回]
    tokuzu1 = 50
    # 特図2当せん時の電サポ回数[回]
    tokuzu2 = 80
    return normal, koukaku, tokuzu1, tokuzu2
```

こんな感じです。  
確変ループ機は`tokuzu1`,`tokuzu2`は不要です。


### furiwake_heso
特図1の振り分けです。確変か通常か等の判定に必要です。

たとえば、V-ST機だと 
```python
def furiwake_heso():
    # ダンバインの特図1の振り分けは50.8%が4R確変。
    # 49.2%が3R通常
    a = random.randint(0, 1000)
    if a < 508:
        heso = "4R(確変)"
    else:
        heso = "3R(通常)"
    return heso
```
こんな感じです。  

### furiwake_denchu
特図2の振り分けです。  
確変ループ機の場合は確変か通常か等の判定に必要です。

たとえば、V-ST機だと 
```python
def furiwake_denchu():
    # ここはラウンド振り分け。
    # ダンバインは12Rが15%,8Rが35%,4Rが50%
    a = random.randint(0, 100)
    if a < 50:
        denchu = "4R（連荘）"
    elif a >= 50 and a < 85:
        denchu = "8R（連荘）"
    else:
        denchu = "12R（連荘）"
    return denchu
```

確変ループ機は毛色が異なります。

```python
def furiwake_denchu():
    # ここはラウンド振り分け。
    # 冬ソナは50%が10R確変。10%が2R確変。40%が10R通常
    a = random.randint(0, 100)
    if a < 50:
        denchu = "10R（確変）"
        kakuhen = True
    elif a >= 50 and a < 60:
        denchu = "2R（確変）"
        kakuhen = True
    else:
        denchu = "10R（通常）"
        kakuhen = False
    return denchu, kakuhen

```

### migiuchi_judge
V-ST機と1種2種混合機のみ必要です。  
時短なしか時短ありか等を抽せんします。

V-ST機は、

```python
def migiuchi_judge(heso):
    # 確変突入率のジャッジ
    # ダンバインは50.8%で右打ち
    if heso == "4R(確変)":
        judge = 1
    else :
        judge = 2
    return judge
```

1種2種混合機は
```python
def migiuchi_judge(heso):
    # 確変突入率のジャッジ
    # シンフォギアは100%時短あり
    judge = 0
    return judge

```
```python
def migiuchi_judge(heso):
    # 確変突入率のジャッジ
    # 大工の源さんは60.2%で右打ち
    if heso == "6R(確変)":
        judge = 1
    else :
        judge = 2
    return judge

```

と書きます。
