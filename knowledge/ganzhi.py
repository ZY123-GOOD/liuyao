# knowledge/ganzhi.py

STEMS=[

"甲","乙","丙","丁","戊",
"己","庚","辛","壬","癸"

]

BRANCHES=[

"子","丑","寅","卯","辰","巳",
"午","未","申","酉","戌","亥"

]


def ganzhi_day(index):

    stem=STEMS[index%10]

    branch=BRANCHES[index%12]

    return stem+branch