from math import inf
import random
import pandas as pd
import sys
import matplotlib.pyplot as plt
# %matplotlib inline

"""
転落機
Pフィーバー機動戦士ガンダムユニコーン
大当り確率	1/319.7→約1/41.1（※1）
RUSH突入率	60%
RUSH継続率（※2）	約81%
転落小当り確率（※3）	約1/153.7
賞球数	3&1&5&15
ラウンド	3R or 10R
カウント	10カウント
出玉	450 or 1500個
※払い出し
電サポ	次回大当りorバトル敗北まで

大当り割合
特図1	ラウンド	電サポ	比率
10R×2回	RUSH	20%
3R	RUSH	40%
3R	ー	40%
特図2A（※1）	ラウンド	電サポ	比率
10R	RUSH	100%
特図2B（※2）	ラウンド	電サポ	比率
10R	覚醒HYPER	100%
※1…特図2A＝大当り2回目（初回含む）まで。
※2…特図2B＝大当り3回目以降。
"""

def information():
    codename = "P_UNICORN"
    # 低確率状態での大当たり確率[1/n]
    normal = 319.7
    # 高確率状態での小当たり確率[1/n]
    koukaku = 41.1
    # 転落小当たり確率
    tenraku = 153.7
    # 賞球（ヘソ、電チュー、一般入賞口、アタッカー、カウント）
    syokyu = [3, 1, 5, 15, 10]
    return normal, koukaku, syokyu, tenraku,codename

def furiwake_heso():
    a = random.randint(0, 100)
    if a < 20:
        furiwake = "10R*2（確変）"
        kakuhen = True
        densapo = True
        round = 20
        kakuhen_time = 9999
        jitan_time = 9999
    elif a >= 20 and a < 60:
        furiwake = "3R（確変）"
        kakuhen = True
        densapo = True
        round = 3
        kakuhen_time = 9999
        jitan_time = 9999
    else:
        furiwake = "3R（通常）"
        kakuhen = False
        densapo = True
        round = 3
        kakuhen_time = 0
        jitan_time = 0
    return furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time

def furiwake_denchu():
    furiwake = "10R（確変）"
    kakuhen = True
    densapo = True
    round = 10
    kakuhen_time = 70
    jitan_time = 70
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


def random_select(normal, koukaku, tenraku):
    # 乱数設定を行う。大当たり確率は65536個中のX個で決定している。
    heso_ran = 1 / normal * 65536
    heso_ran = int(heso_ran)
    denchu_ran = 1 / koukaku * 65536
    denchu_ran = int(denchu_ran)
    tenraku_ran = 1 / tenraku * 65536
    tenraku_ran = int(tenraku_ran)
    # 乱数生成
    a = list(range(0, 65536))
    heso_atari = random.sample(a, heso_ran)
    denchu_atari = random.sample(a, denchu_ran)
    tenraku_atari = random.sample(a, tenraku_ran)
    return heso_atari, denchu_atari, tenraku_atari


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


def chusen_koukaku(tokuzu2_atari, tenraku_atari):
    # 特図2での抽せん
    lottery = random.randint(0, 65536)
    if not lottery in tenraku_atari:
        if lottery in tokuzu2_atari:
            # 大当たり
            result = 1
        else:
            # はずれ
            result = 0
    else :
        # 転落小当たり
        result = 2
    return result


def calc_border(border):
    # ボーダーの計算
    # 250玉あたりの回転数の逆数を取る
    cost_1tama = 250 / int(border)
    return cost_1tama

def main(trials:int, border:int):
    # 機種情報読み込み
    normal, koukaku, syokyu, tenraku, machinename = information()
    # 試行回数
    challenge = int(trials)
    # ボーダーの計算
    cost_border = calc_border(border)
    # 確認
    print("低確率：1/" + str(normal))
    print("高確率：1/" + str(koukaku))
    # 乱数設定
    heso, denchu, tenraku = random_select(normal, koukaku, tenraku)
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
                kekka = chusen_koukaku(denchu, tenraku)
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
        elif kekka == 1 :
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
        else :
            # 転落
            kakuhen = False
            densapo = False
            kaiten = 0
            kaiten_sum = kaiten_sum + 1
            # 泣きの4回
            for i in range(4):
                kekka = chusen_koukaku(denchu, tenraku)
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
