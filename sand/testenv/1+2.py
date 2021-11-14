from math import inf
import random
import pandas as pd
import sys
import matplotlib.pyplot as plt
import importlib
from utils.validate_args import is_valid_args
# %matplotlib inline

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

def main(machine_name: str, trials: int, border:int):
    # 機種情報読み込み
    """
    1種2種混合機

    :param string machine_name: 機種名
    :param int trials: 試行回数
    :return: None
    """

    # 指定された機種を読み込み.
    machine = importlib.import_module(f'machine.{machine_name}')
    normal, koukaku, syokyu, tenraku, machinename = machine.information()
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
                furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time = machine.furiwake_heso()
                record = pd.Series([kaiten_sum, kaiten, furiwake, sadama], index=result.columns)
                result = result.append(record, ignore_index=True)
            else : 
                furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time = machine.furiwake_denchu()
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
                    furiwake, kakuhen, densapo, round, kakuhen_time, jitan_time = machine.furiwake_denchu()
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
    if len(args) < 4:
        print("Error.\n<Usage>\npython3 1+2mix.py <機種名> <試行回数> <ボーダー>")
        sys.exit('error: invalid args')
    elif not is_valid_args(args[1], args[2], args[3]):
        # バリデーションエラーの場合
        sys.exit('error: invalid args')

    machine_name = args[1]
    trials = int(args[2])
    border = float(args[3])

    main(machine_name, trials, border)
