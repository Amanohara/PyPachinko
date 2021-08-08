import random

'''
確変ループ機
ぱちんこ 冬のソナタ FOREVER
'''

def main():
    pass

def information():
    # 特図1での大当たり確率[1/n]
    normal = 319.9
    # 特図2での大当たり確率[1/n]
    koukaku = 39.7
    # 特図1当せん時の電サポ回数[回]
    ''' 次回まで'''
    # 特図2当せん時の電サポ回数[回]
    ''' 次回まで'''
    # 時短回数
    jitan = 100
    return normal, koukaku, jitan


def furiwake_heso():
    # 冬ソナの特図１の振り分けは40%が10R確変。20%が2R確変。40%が10R通常
    a = random.randint(0, 100)
    if a < 40:
        heso = "10R(確変)"
        kakuhen = True
    elif a >= 40 and a < 60:
        heso = "2R(確変)"
        kakuhen = True
    else:
        heso = "10R(通常)"
        kakuhen = False
    return heso, kakuhen


def furiwake_denchu():
    # ここはラウンド振り分け。
    # 冬ソナは50%が10R確変。10%が2R確変。40%が10R通常
    a = random.randint(0, 100)
    if a < 50:
        denchu = "10R（確変）"
        kakuhen = True
    elif a >= 50 and a < 60:
        denchu = "2R（確変）"
        kakuhen = True
    else:
        denchu = "10R（通常）"
        kakuhen = False
    return denchu, kakuhen

if __name__ == '__main__':
    main()