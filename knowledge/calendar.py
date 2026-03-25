import sxtwl

STEMS=[

"甲","乙","丙","丁","戊",
"己","庚","辛","壬","癸"

]

BRANCHES=[

"子","丑","寅","卯","辰","巳",
"午","未","申","酉","戌","亥"

]


def get_day_branch(dt):

    day=sxtwl.fromSolar(

    dt.year,
    dt.month,
    dt.day

    )

    gz=day.getDayGZ()

    return BRANCHES[gz.dz]


def get_month_branch(dt):

    day=sxtwl.fromSolar(

    dt.year,
    dt.month,
    dt.day

    )

    gz=day.getMonthGZ()

    return BRANCHES[gz.dz]