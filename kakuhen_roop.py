import random
import pandas as pd
import sys
import importlib

'''
確変ループ機
'''


def main(machine_name: str, trials: int):
    # 指定された機種を読み込み.
    machine = importlib.import_module(f'machine.{machine_name}')

    normal, koukaku, jitan = machine.information()
    # 試行回数
    challenge = int(trials)
    # 確認
    print("低確率：1/" + str(normal))
    print("高確率：1/" + str(koukaku))
    # 乱数設定
    heso, denchu = random_select(normal, koukaku)
    # ラムクリア
    kaiten, kaiten_sum, mode = ram_clear()
    # 大当たり表の枠作成
    result = create_flame()
    # ここから抽せん開始。。
    for i in range(0, challenge):
        # 高確率か低確率か時短中かを判定する
        if mode == "normal":
            kekka = chusen_normal(heso)
        elif mode == "koukaku":
            kekka = chusen_koukaku(denchu)
        else:
            # 時短
            kekka = chusen_jitan(denchu, kaiten, jitan)
        # 0ははずれ。何もせずに回転数を足す
        # 1は特図1での大当たり。電サポをtokuzu1回す
        # 2は特図2での大当たり。電サポをtokuzu2回す
        # 9は左打ちに戻す
        if kekka == 0:
            # はずれ
            kaiten = kaiten + 1
            kaiten_sum = kaiten_sum + 1
        elif kekka == 1:
            # 特図１での大当たり。振り分け判定。
            furiwake, kakuhen_mode = machine.furiwake_heso()
            # 回転数を記録後、リセット
            record = pd.Series([kaiten, furiwake, kaiten_sum], index=result.columns)
            result = result.append(record, ignore_index=True)
            kaiten = 0
            kaiten_sum = kaiten_sum + 1
            # 振り分けにより次回モードを変更
            if kakuhen_mode == True:
                # 確変
                mode = "koukaku"
            else:
                # 時短
                mode = "jitan"

        elif kekka == 2:
            # 特図2大当たり。振り分け判定。
            furiwake, kakuhen_mode = machine.furiwake_denchu()
            # 回転数を記録後、リセット
            record = pd.Series([kaiten, furiwake, kaiten_sum], index=result.columns)
            result = result.append(record, ignore_index=True)
            kaiten = 0
            kaiten_sum = kaiten_sum + 1
            # 振り分けにより次回モードを変更
            if kakuhen_mode == True:
                # 確変
                mode = "koukaku"
            else:
                # 時短
                mode = "jitan"
        else:
            # kekka==9を想定。不承不承ながら左打ち
            mode = "normal"
    result.to_csv("result.csv", index=None)


def ram_clear():
    # ラムクリア
    kaiten = 0
    kaiten_sum = 0
    mode = "normal"
    return kaiten, kaiten_sum, mode


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
    cols = ['回転数', '大当たり', '総回転数']
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
        result = 2
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


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print("Error.\n<Usage>\npython3 kakuhen_roop.py <機種名> <試行回数>")
    else:
        machine_name = args[1]
        trials = int(args[2])
        main(machine_name, trials)
