from math import inf
import random
import pandas as pd
import sys
import matplotlib.pyplot as plt
# %matplotlib inline

"""
Pスーパー海物語 IN 沖縄5
大当り確率	約1/319.6→約1/38.0
確変突入率	60%
賞球数	3&2&4&15
ラウンド	2R or 10R
カウント	10カウント
出玉	90 or 1500個
※払い出し
時短	100 or 120回

大当り割合
ヘソ	ラウンド	電サポ回数	比率
10R確変	次回まで	40%
2R確変	次回まで	20%
10R通常	100回	40%
電チュー	ラウンド	電サポ回数	比率
10R確変	次回まで	52%
2R確変	次回まで	8%
10R通常	120回	40%
"""

def information():
    codename = "P_okiumi5"
    # 低確率状態での大当たり確率[1/n]
    normal = 319.6
    # 高確率状態での大当たり確率[1/n]
    koukaku = 38.0
    # 賞球（ヘソ、電チュー、一般入賞口、アタッカー、カウント）
    syokyu = [3, 2, 4, 15, 10]
    return normal, koukaku, syokyu, codename

def furiwake_heso():
    a = random.randint(0, 100)
    if a < 40:
        furiwake = "10R（確変）"
        kakuhen = True
        densapo = True
        round = 10
        kakuhen_time = 9999
        jitan_time = 9999
    elif a >= 40 and a < 60:
        furiwake = "2R（確変）"
        kakuhen = True
        densapo = True
        round = 2
        kakuhen_time = 9999
        jitan_time = 9999
    else:
        furiwake = "10R（通常）"
        kakuhen = False
        densapo = True
        round = 10
        kakuhen_time = 0
        jitan_time = 100
    return furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time

def furiwake_denchu():
    a = random.randint(0, 100)
    if a < 52:
        furiwake = "10R（確変）"
        kakuhen = True
        densapo = True
        round = 10
        kakuhen_time = 9999
        jitan_time = 9999
    elif a >= 52 and a < 60:
        furiwake = "2R（確変）"
        kakuhen = True
        densapo = True
        round = 2
        kakuhen_time = 9999
        jitan_time = 9999
    else:
        furiwake = "10R（通常）"
        kakuhen = False
        densapo = True
        round = 10
        kakuhen_time = 0
        jitan_time = 120
    return furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time

def ram_clear():
    # ラムクリア
    kaiten = 0
    kaiten_sum = 0
    kakuhen = False
    densapo = False
    kakuhen_time = 0
    jitan_time = 0
    return kaiten, kaiten_sum, kakuhen, kakuhen_time, densapo, jitan_time


def random_select(normal, koukaku):
    # 乱数設定を行う。大当たり確率は65536個中のX個で決定している。
    heso_ran = 1 / normal * 65536
    heso_ran = int(heso_ran)
    denchu_ran = 1 / koukaku * 65536
    denchu_ran = int(denchu_ran)
    # 乱数生成
    a = list(range(0, 65536))
    heso_atari = random.sample(a, heso_ran)
    denchu_atari = random.sample(a, denchu_ran)
    return heso_atari, denchu_atari


def create_flame():
    # Pandasフレームの作成
    cols = ['総回転数', '回転数', '大当たり', '差玉']
    df = pd.DataFrame(index=[], columns=cols)
    return df


def chusen_normal(tokuzu1):
    # 特図１での抽せん
    lottery = random.randint(0, 65536)
    if lottery in tokuzu1:
        # 大当たり
        result = 1
    else:
        # はずれ
        result = 0
    return result


def chusen_koukaku(tokuzu2_atari):
    # 特図2での抽せん
    lottery = random.randint(0, 65536)
    if lottery in tokuzu2_atari:
        # 大当たり
        result = 1
    else:
        # はずれ
        result = 0
    return result


def chusen_jitan(tokuzu1_atari, kaiten, limit):
    # 時短中の扱い
    if kaiten <= limit:
        lottery = random.randint(0, 65536)
        if lottery in tokuzu1_atari:
            # 大当たり
            result = 2
        else:
            # はずれ
            result = 0
    else:
        # 左打ちに戻す信号を送る
        result = 9
    return result

def calc_border(border):
    # ボーダーの計算
    # 250玉あたりの回転数の逆数を取る
    cost_1tama = 250 / int(border)
    return cost_1tama

def main(trials:int, border:int):
    # 機種情報読み込み
    normal, koukaku, syokyu, machinename = information()
    # 試行回数
    challenge = int(trials)
    # ボーダーの計算
    cost_border = calc_border(border)
    # 確認
    print("低確率：1/" + str(normal))
    print("高確率：1/" + str(koukaku))
    # 乱数設定
    heso, denchu = random_select(normal, koukaku)
    # ラムクリア
    kaiten, kaiten_sum, kakuhen,kakuhen_time,  densapo, jitan_time = ram_clear()
    sadama = 0
    # 大当たり表の枠作成
    result = create_flame()

    # ここから抽せん開始。。
    for i in range(0, challenge):
        # 電サポ回数を確認。規定回数を超えていたら左打ち
        if kaiten >= jitan_time :
            densapo = False
        # 高確率か低確率か判定し抽せん
        if kakuhen == False:
            # 低確率
            kekka = chusen_normal(heso)
        else:
            # 高確率
            if kaiten < kakuhen_time:
                kekka = chusen_normal(denchu)
            else :
                # ST終了時を想定
                kakuhen = False
                kekka = chusen_normal(heso)
        # 0ははずれ。回転数を足す
        # 1は当たり。振り分けを行う
        if kekka ==  0 :
            # はずれ
            kaiten = kaiten + 1
            kaiten_sum = kaiten_sum + 1
            # 電サポではないときは差玉をマイナスにする
            if densapo == False :
                sadama = sadama - int(cost_border)
        else :
            # 大当たり
            # 通常時なら特図1振り分け
            # 電サポ中なら特図2振り分け
            if densapo == False:
                furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time = furiwake_heso()
                record = pd.Series([kaiten_sum, kaiten, furiwake, sadama], index=result.columns)
                result = result.append(record, ignore_index=True)
            else : 
                furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time = furiwake_denchu()
                record = pd.Series([kaiten_sum, kaiten, furiwake, sadama], index=result.columns)
                result = result.append(record, ignore_index=True)
            # 大当たり時の出玉の計算
            # アタッカー賞球 * ラウンドを足せばよい
            dedama = syokyu[3] * syokyu[4] * round
            sadama = sadama + dedama
            # 回転数を記録後、リセット
            kaiten = 0
            kaiten_sum = kaiten_sum + 1
    result.to_csv("result.csv", index=None)
    # グラフを描く。描くのは総回転数と出玉。タイトルには機種名と試行回数とボーダーを載せる
    title = str(machinename)+ "(N=" + str(trials) + ",border=" + str(border) + ")"
    fig = result.plot(x = '総回転数', y = '差玉', title = title, legend=False )
    plt.savefig("result.pdf")
    plt.savefig("result.png")


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print("なにかがおかしいよ")
    else :
        trials = args[1]
        border = args[2]
        main(trials ,border)
