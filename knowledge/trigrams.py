# knowledge/trigrams.py

TRIGRAMS={

(1,1,1):"乾",
(0,0,0):"坤",

(0,1,0):"坎",
(1,0,1):"离",

(1,0,0):"震",
(0,0,1):"艮",

(1,1,0):"兑",
(0,1,1):"巽"

}


def get_trigram(lines):

    """
    lines 3个阴阳爻
    1阳
    0阴
    """

    return TRIGRAMS.get(tuple(lines))

def to_yinyang(value):

    if value in [7,9]:

        return 1

    return 0