import random

'''
1種2種混合機
P大工の源さん超韋駄天
'''


def main():
    pass


def information():
    # 特図1での大当たり確率[1/n]
    normal = 319.68
    # 特図2での小当たり確率[1/n]
    koukaku = 2.07
    # 特図1当せん時の電サポ回数[回]
    tokuzu1 = 0
    # 特図2当せん時の電サポ回数[回]
    tokuzu2 = 4
    return normal, koukaku, tokuzu1, tokuzu2


def furiwake_heso():
    # 大工の源さんの特図１の振り分けは60.2%が6R確変。39.8%は6R通常
    a = random.randint(0, 1000)
    if a < 602:
        heso = "6R(確変)"
    else:
        heso = "6R(通常)"
    return heso


def furiwake_denchu():
    # ここはラウンド振り分け。
    # 大工の源さんは3Rが80%,9Rが20%
    a = random.randint(0, 100)
    if a < 80:
        denchu = "3R（連荘）"
    else:
        denchu = "9R（連荘）"
    return denchu


def migiuchi_judge(heso):
    # 確変突入率のジャッジ
    # 大工の源さんは60.2%で右打ち
    if heso == "6R(確変)":
        judge = 1
    else:
        judge = 2
    return judge


if __name__ == '__main__':
    main()
