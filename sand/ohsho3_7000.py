from math import inf
import random
import pandas as pd
import sys
import matplotlib.pyplot as plt
# %matplotlib inline

"""
CR餃子の王将3 メガ盛り7000
大当り確率	1/35.8→1/9.6
小当たり確率	1/34.7
確変突入率	100%(63回ワンセット)
賞球数	3&1&6&10&15
ラウンド	2R
カウント	4カウント
出玉	約7560個　※払い出し
"""

def information():
    codename = "CR_OHSHO3_7000"
    # 低確率状態での大当たり確率[1/n]
    normal = 35.8
    # 高確率状態での大当たり確率[1/n]
    koukaku = 9.6
    # 小当たり確率[1/n]
    koatari = 34.7
    # 賞球（ヘソ、電チュー、一般入賞口、アタッカー、カウント）
    syokyu = [3, 1, 6, 15, 4]
    return normal, koukaku, syokyu, codename

def furiwake_heso():
    furiwake = "2R"
    kakuhen = True
    densapo = True
    round = 2
    kakuhen_time = 9999
    jitan_time = 9999
    return furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time

def furiwake_denchu():
    furiwake = "2R(右打ち)"
    kakuhen = True
    densapo = True
    round = 2
    kakuhen_time = 9999
    jitan_time = 9999
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
    cost_1tama = 250 / float(border)
    return int(cost_1tama)

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
    print("ボーダー：1k"+ str(cost_border) + "回転")
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
        # 高確率か低確率か判定し抽せん
        kekka = chusen_normal(heso)
        # 0ははずれ。回転数を足す
        # 1は当たり。振り分けを行う
        if kekka ==  0 :
            # はずれ
            kaiten = kaiten + 1
            kaiten_sum = kaiten_sum + 1
            sadama = sadama - int(cost_border)
        else :
            # 大当たり（63回リミッタ）
            furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time = furiwake_heso()
            record = pd.Series([kaiten_sum, kaiten, furiwake, sadama], index=result.columns)
            result = result.append(record, ignore_index=True)
            dedama = syokyu[3] * syokyu[4] * round
            sadama = sadama + dedama
            kaiten = 0
            kaiten_sum += 1
            i = 1
            while i < 63:
                if i == 62 :
                    densapo = False
                    kakuhen = False
                    j = 0
                    while j < 4 :
                        kekka = chusen_normal(heso)
                        if kekka == 1 :
                            # おかわり成功
                            furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time = furiwake_heso()
                            record = pd.Series([kaiten_sum, kaiten, furiwake, sadama], index=result.columns)
                            result = result.append(record, ignore_index=True)
                            dedama = syokyu[3] * syokyu[4] * round
                            sadama = sadama + dedama
                            kaiten = 0
                            kaiten_sum += 1
                            i = 0
                            break
                        else :
                            kaiten += 1
                            kaiten_sum += 1
                            j += 1
                else :
                    kekka = chusen_normal(denchu)
                    if kekka == 1 :
                        # 大当たり
                        i += 1
                        furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time = furiwake_denchu()
                        record = pd.Series([kaiten_sum, kaiten, furiwake, sadama], index=result.columns)
                        result = result.append(record, ignore_index=True)
                        dedama = syokyu[3] * syokyu[4] * round
                        sadama = sadama + dedama
                        kaiten = 0
                        kaiten_sum += 1
                    else :
                        kaiten += 1
                        kaiten_sum += 1
                
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
