# knowledge/branches.py

# 地支五行

BRANCH_ELEMENT = {

"子":"水",

"丑":"土",

"寅":"木",

"卯":"木",

"辰":"土",

"巳":"火",

"午":"火",

"未":"土",

"申":"金",

"酉":"金",

"戌":"土",

"亥":"水"

}


# 六冲

CLASH = {

("子","午"),

("丑","未"),

("寅","申"),

("卯","酉"),

("辰","戌"),

("巳","亥")

}


# 六合

COMBINE = {

("子","丑"),

("寅","亥"),

("卯","戌"),

("辰","酉"),

("巳","申"),

("午","未")

}


def get_element(branch):

    return BRANCH_ELEMENT.get(branch,"土")


def is_clash(b1,b2):

    return (

        (b1,b2) in CLASH

        or

        (b2,b1) in CLASH

    )


def is_combine(b1,b2):

    return (

        (b1,b2) in COMBINE

        or

        (b2,b1) in COMBINE

    )