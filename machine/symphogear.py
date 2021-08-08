import random

'''
1種2種混合機
CRF戦姫絶唱シンフォギア
'''

def main():
    pass

def information():
    # 特図1での大当たり確率[1/n]
    normal = 199.8
    # 特図2での小当たり確率[1/n]
    koukaku = 7.4
    # 特図1当せん時の電サポ回数[回]
    tokuzu1 = 5
    # 特図2当せん時の電サポ回数[回]
    tokuzu2 = 11
    return normal, koukaku, tokuzu1, tokuzu2


def furiwake_heso():
    # シンフォギアの特図１の振り分けは99%が通常。1%は右打ち直行
    a = random.randint(0, 100)
    if a != 50:
        heso = "4R"
    else:
        heso = "全回転"
    return heso


def furiwake_denchu():
    # ここはラウンド振り分け。
    # シンフォギアは4Rが50%,8Rが7%,12Rが3%,15Rが40%
    a = random.randint(0, 100)
    if a < 50:
        denchu = "4R（確変）"
    elif a >= 50 and a < 57:
        denchu = "7R（確変）"
    elif a >= 57 and a < 60:
        denchu = "12R（確変）"
    else:
        denchu = "15R（確変）"
    return denchu

def migiuchi_judge(heso):
    # 確変突入率のジャッジ
    # シンフォギアは100%右打ち
    judge = 0
    return judge

if __name__ == '__main__':
    main()