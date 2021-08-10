import random
import pandas as pd
import sys
import importlib

from utils.validate_args import is_valid_args

'''
1種2種混合機
'''


def main(machine_name: str, trials: int):
    """
    1種2種混合機

    :param string machine_name: 機種名
    :param int trials: 試行回数
    :return: None
    """

    # 指定された機種を読み込み.
    machine = importlib.import_module(f'machine.{machine_name}')

    normal, koukaku, tokuzu1, tokuzu2 = machine.information()
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
        # 高確率か低確率か最終決戦中かを判定する
        if mode == "normal":
            kekka = chusen_normal(heso)
        elif mode == "koukaku":
            kekka = chusen_koukaku(heso, denchu, kaiten, tokuzu2)
        else:
            # 最終決戦(搭載機による)
            kekka = chusen_fine(denchu, kaiten, tokuzu1)
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
            furiwake = machine.furiwake_heso()
            # 回転数を記録後、リセット
            record = pd.Series([kaiten, furiwake, kaiten_sum], index=result.columns)
            result = result.append(record, ignore_index=True)
            kaiten = 0
            kaiten_sum = kaiten_sum + 1
            '''
            時短突入抽せん
            0はシンフォギアスペック(突破型）
            1は時短突入率で判定かつ当せん
            2は時短突入率で判定かつ通常
            '''
            migiuchi = machine.migiuchi_judge(furiwake)
            if migiuchi == 0:
                # 最終決戦突入。ただし振り分けで1％を引くと高確率直行
                if furiwake != "全回転":
                    mode = "fine"
                else:
                    mode = "koukaku"
            elif migiuchi == 1:
                # 時短突入
                mode = "koukaku"
            else:
                # 通常
                mode = "normal"
        elif kekka == 2:
            # 特図2大当たり。振り分け判定。
            furiwake = machine.furiwake_denchu()
            # 回転数を記録後、リセット
            record = pd.Series([kaiten, furiwake, kaiten_sum], index=result.columns)
            result = result.append(record, ignore_index=True)
            kaiten = 0
            kaiten_sum = kaiten_sum + 1
            # 次回も高確率
            mode = "koukaku"
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


def chusen_koukaku(tokuzu1_atari, tokuzu2_atari, kaiten, limit):
    # 特図2での抽せん
    if kaiten <= limit:
        lottery = random.randint(0, 65536)
        if lottery in tokuzu2_atari or lottery in tokuzu1_atari:
            # 大当たり
            result = 2
        else:
            # はずれ
            result = 0
    else:
        # 左打ちに戻す信号を送る
        result = 9
    return result


def chusen_fine(tokuzu2_atari, kaiten, limit):
    # 最終決戦中の扱い
    if kaiten <= limit:
        lottery = random.randint(0, 65536)
        if lottery in tokuzu2_atari:
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
        print("Error.\n<Usage>\npython3 1+2mix.py <機種名> <試行回数>")
        sys.exit('error: invalid args')
    elif not is_valid_args(args[1], args[2]):
        # バリデーションエラーの場合
        sys.exit('error: invalid args')

    machine_name = args[1]
    trials = int(args[2])

    main(machine_name, trials)
