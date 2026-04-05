# engine/coin.py

import random

def toss():

    """
    模拟三枚铜钱

    3 正 = 老阳 (9)
    2 正 = 少阴 (8)
    2 反 = 少阳 (7)
    3 反 = 老阴 (6)
    """

    coins=[random.choice([2,3]) for _ in range(3)]

    total=sum(coins)

    if total==9:
        return 9

    if total==8:
        return 8

    if total==7:
        return 7

    return 6


def build_hexagram():

    """
    生成六爻（从下往上）
    """

    lines=[]

    for i in range(6):

        lines.append(toss())

    return lines