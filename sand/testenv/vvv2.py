from math import inf
import random
import pandas as pd
import sys
import matplotlib.pyplot as plt
# %matplotlib inline

"""
Pフィーバー革命機ヴァルヴレイヴ2
大当り確率	1/319.7→1/32.0
確変突入率	特図1：50%　特図2：94%
(ST70回)（※1）
RUSH突入率	約58%（※2）
RUSH継続率	約90%（※3）
賞球数	3&1&5&15
ラウンド	2R or 3R or 4R or 7R or 10R
カウント	10カウント
出玉	約300 or 450 or 600 or
1050 or 1500個
※払い出し
電サポ	8 or 70 or 100 or 10000回

大当り割合
特図1	ラウンド	電サポ回数	比率
10R確変	70回	25%
3R確変	70回	13%
3R確変	8回（※1）（※2）	12%
3R通常	100回	39%
3R通常	8回（※3）	11%

特図2	ラウンド	電サポ回数	比率
10R確変	70回	7%
7R確変	70回	31%
4R確変	70回	25%
2R確変	70回	31%
7R通常	10000回	2%
4R通常	10000回	2%
2R通常	10000回	2%
※1…ST残り62回は電サポなし。
※2…高確中は電サポ70回。
※3…高確中は電サポ100回。
"""

def information():
    codename = "P_VVV2"
    # 低確率状態での大当たり確率[1/n]
    normal = 319.7
    # 高確率状態での大当たり確率[1/n]
    koukaku = 32.0
    # 賞球（ヘソ、電チュー、一般入賞口、アタッカー、カウント）
    syokyu = [3, 1, 5, 15, 10]
    return normal, koukaku, syokyu, codename

def furiwake_heso():
    a = random.randint(0, 100)
    if a < 25:
        furiwake = "10R（確変）"
        kakuhen = True
        densapo = True
        round = 10
        kakuhen_time = 70
        jitan_time = 70
    elif a >= 25 and a < 38:
        furiwake = "3R（確変）"
        kakuhen = True
        densapo = True
        round = 3
        kakuhen_time = 70
        jitan_time = 70
    elif a >= 38 and a < 50:
        furiwake = "3R（確変）"
        kakuhen = True
        densapo = True
        round = 3
        kakuhen_time = 70
        jitan_time = 8
    elif a >= 50 and a < 89:
        furiwake = "3R（通常）"
        kakuhen = False
        densapo = True
        round = 3
        kakuhen_time = 0
        jitan_time = 100
    else:
        furiwake = "3R（通常）"
        kakuhen = False
        densapo = True
        round = 3
        kakuhen_time = 0
        jitan_time = 8
    return furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time

def furiwake_denchu():
    a = random.randint(0, 100)
    if a < 7:
        furiwake = "10R（確変）"
        kakuhen = True
        densapo = True
        round = 10
        kakuhen_time = 70
        jitan_time = 70
    elif a >= 7 and a < 38:
        furiwake = "7R（確変）"
        kakuhen = True
        densapo = True
        round = 7
        kakuhen_time = 70
        jitan_time = 70
    elif a >= 38 and a < 63:
        furiwake = "4R（確変）"
        kakuhen = True
        densapo = True
        round = 4
        kakuhen_time = 70
        jitan_time = 70
    elif a >= 63 and a < 94:
        furiwake = "2R（確変）"
        kakuhen = True
        densapo = True
        round = 2
        kakuhen_time = 70
        jitan_time = 70
    elif a >= 94 and a < 96:
        furiwake = "7R（通常）"
        kakuhen = False
        densapo = True
        round = 7
        kakuhen_time = 0
        jitan_time = 10000
    elif a >= 96 and a < 98:
        furiwake = "4R（通常）"
        kakuhen = False
        densapo = True
        round = 4
        kakuhen_time = 0
        jitan_time = 10000
    else:
        furiwake = "2R（通常）"
        kakuhen = False
        densapo = True
        round = 2
        kakuhen_time = 0
        jitan_time = 10000
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
                # 泣きの4回（残保留）
                for i in range(4):
                    kekka = chusen_normal(heso)
                    if kekka == 1 :
                        # 引き戻し
                        furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time = furiwake_denchu()
                        record = pd.Series([kaiten_sum, kaiten, furiwake, sadama], index=result.columns)
                        result = result.append(record, ignore_index=True)
                        # 大当たり時の出玉の計算
                        # アタッカー賞球 * ラウンドを足せばよい
                        dedama = syokyu[3] * syokyu[4] * round
                        sadama = sadama + dedama
                        kaiten = 0
                        kaiten_sum = kaiten_sum + 1
                        break
                    else:
                        kaiten = 0
                        kaiten_sum = kaiten_sum + 1
                kakuhen = False
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
