import random

'''
V-ST機
ぱちんこCR聖戦士ダンバインFWN
'''


def main():
    pass


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


def furiwake_heso():
    # ダンバインの特図１の振り分けは50.8%が4R確変。49.2%が3R通常
    a = random.randint(0, 1000)
    if a < 508:
        heso = "4R(確変)"
    else:
        heso = "3R(通常)"
    return heso


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


def migiuchi_judge(heso):
    # 確変突入率のジャッジ
    # ダンバインは50.8%で右打ち
    if heso == "4R(確変)":
        judge = 1
    else:
        judge = 2
    return judge


if __name__ == '__main__':
    main()
