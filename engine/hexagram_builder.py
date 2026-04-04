from knowledge.trigrams import to_yinyang
from knowledge.trigrams import get_trigram

from knowledge.najia import get_branches

from engine.state import Line


# 64卦 卦宫 + 世应表（核心修复）
# key = (下卦, 上卦)

HEXAGRAM_INFO = {

# -------- 乾宫 --------

("乾","乾"):{"name":"乾","palace":"乾","shi":6,"ying":3},
("巽","乾"):{"name":"姤","palace":"乾","shi":1,"ying":4},
("艮","乾"):{"name":"遁","palace":"乾","shi":2,"ying":5},
("坤","乾"):{"name":"否","palace":"乾","shi":3,"ying":6},
("震","乾"):{"name":"观","palace":"乾","shi":4,"ying":1},
("离","乾"):{"name":"剥","palace":"乾","shi":5,"ying":2},
("兑","乾"):{"name":"晋","palace":"乾","shi":4,"ying":1},
("坎","乾"):{"name":"大有","palace":"乾","shi":3,"ying":6},

# -------- 兑宫 --------

("兑","兑"):{"name":"兑","palace":"兑","shi":6,"ying":3},
("坎","兑"):{"name":"困","palace":"兑","shi":1,"ying":4},
("坤","兑"):{"name":"萃","palace":"兑","shi":2,"ying":5},
("震","兑"):{"name":"咸","palace":"兑","shi":3,"ying":6},
("乾","兑"):{"name":"蹇","palace":"兑","shi":4,"ying":1},
("巽","兑"):{"name":"大过","palace":"兑","shi":5,"ying":2},
("离","兑"):{"name":"随","palace":"兑","shi":4,"ying":1},
("艮","兑"):{"name":"夬","palace":"兑","shi":3,"ying":6},

# -------- 离宫 --------

("离","离"):{"name":"离","palace":"离","shi":6,"ying":3},
("艮","离"):{"name":"旅","palace":"离","shi":1,"ying":4},
("乾","离"):{"name":"鼎","palace":"离","shi":2,"ying":5},
("兑","离"):{"name":"未济","palace":"离","shi":3,"ying":6},
("坎","离"):{"name":"蒙","palace":"离","shi":4,"ying":1},
("坤","离"):{"name":"涣","palace":"离","shi":5,"ying":2},
("震","离"):{"name":"讼","palace":"离","shi":4,"ying":1},
("巽","离"):{"name":"同人","palace":"离","shi":3,"ying":6},

# -------- 震宫 --------

("震","震"):{"name":"震","palace":"震","shi":6,"ying":3},
("坤","震"):{"name":"复","palace":"震","shi":1,"ying":4},
("坎","震"):{"name":"屯","palace":"震","shi":2,"ying":5},
("兑","震"):{"name":"随","palace":"震","shi":3,"ying":6},
("离","震"):{"name":"无妄","palace":"震","shi":4,"ying":1},
("乾","震"):{"name":"明夷","palace":"震","shi":5,"ying":2},
("艮","震"):{"name":"贲","palace":"震","shi":4,"ying":1},
("巽","震"):{"name":"大壮","palace":"震","shi":3,"ying":6},

# -------- 巽宫 --------

("巽","巽"):{"name":"巽","palace":"巽","shi":6,"ying":3},
("乾","巽"):{"name":"小畜","palace":"巽","shi":1,"ying":4},
("离","巽"):{"name":"家人","palace":"巽","shi":2,"ying":5},
("震","巽"):{"name":"益","palace":"巽","shi":3,"ying":6},
("坤","巽"):{"name":"升","palace":"巽","shi":4,"ying":1},
("坎","巽"):{"name":"井","palace":"巽","shi":5,"ying":2},
("兑","巽"):{"name":"大过","palace":"巽","shi":4,"ying":1},
("艮","巽"):{"name":"恒","palace":"巽","shi":3,"ying":6},

# -------- 坎宫 --------

("坎","坎"):{"name":"坎","palace":"坎","shi":6,"ying":3},
("兑","坎"):{"name":"节","palace":"坎","shi":1,"ying":4},
("震","坎"):{"name":"既济","palace":"坎","shi":2,"ying":5},
("离","坎"):{"name":"革","palace":"坎","shi":3,"ying":6},
("巽","坎"):{"name":"丰","palace":"坎","shi":4,"ying":1},
("乾","坎"):{"name":"需","palace":"坎","shi":5,"ying":2},
("坤","坎"):{"name":"比","palace":"坎","shi":4,"ying":1},
("艮","坎"):{"name":"师","palace":"坎","shi":3,"ying":6},

# -------- 艮宫 --------

("艮","艮"):{"name":"艮","palace":"艮","shi":6,"ying":3},
("离","艮"):{"name":"贲","palace":"艮","shi":1,"ying":4},
("巽","艮"):{"name":"渐","palace":"艮","shi":2,"ying":5},
("乾","艮"):{"name":"大畜","palace":"艮","shi":3,"ying":6},
("兑","艮"):{"name":"损","palace":"艮","shi":4,"ying":1},
("坎","艮"):{"name":"蹇","palace":"艮","shi":5,"ying":2},
("坤","艮"):{"name":"谦","palace":"艮","shi":4,"ying":1},
("震","艮"):{"name":"小过","palace":"艮","shi":3,"ying":6},

# -------- 坤宫 --------

("坤","坤"):{"name":"坤","palace":"坤","shi":6,"ying":3},
("震","坤"):{"name":"豫","palace":"坤","shi":1,"ying":4},
("兑","坤"):{"name":"临","palace":"坤","shi":2,"ying":5},
("乾","坤"):{"name":"泰","palace":"坤","shi":3,"ying":6},
("坎","坤"):{"name":"比","palace":"坤","shi":4,"ying":1},
("巽","坤"):{"name":"观","palace":"坤","shi":5,"ying":2},
("艮","坤"):{"name":"剥","palace":"坤","shi":4,"ying":1},
("离","坤"):{"name":"晋","palace":"坤","shi":3,"ying":6},

}

def build(lines, day_element):

    if len(lines) != 6:
        raise ValueError("六爻必须6个")

    yin_yang = [to_yinyang(l) for l in lines]

    lower = get_trigram(yin_yang[:3])
    upper = get_trigram(yin_yang[3:])

    # -------- 纳甲 --------

    lower_branches = get_branches(lower)
    upper_branches = get_branches(upper)

    if not lower_branches or not upper_branches:
        raise ValueError("纳甲失败")

    branches = lower_branches + upper_branches

    if len(branches) != 6:
        raise ValueError("纳甲必须6个")

    original_lines=[]

    for i in range(6):

        n=lines[i]

        original_lines.append(

            Line(
                pos=i+1,
                branch=branches[i],
                day_element=day_element,
                yin_yang=yin_yang[i],
                number=n,
                moving=(n in [6,9])
            )

        )

    # ---------- 变卦 ----------

    transformed_numbers=[]

    for n in lines:

        if n==6:
            transformed_numbers.append(7)

        elif n==9:
            transformed_numbers.append(8)

        else:
            transformed_numbers.append(n)

    transformed_yinyang=[to_yinyang(n) for n in transformed_numbers]

    lower_t=get_trigram(transformed_yinyang[:3])
    upper_t=get_trigram(transformed_yinyang[3:])

    branches_t=get_branches(lower_t)+get_branches(upper_t)

    transformed_lines=[]

    for i in range(6):

        transformed_lines.append(

            Line(
                pos=i+1,
                branch=branches_t[i],
                day_element=day_element,
                yin_yang=transformed_yinyang[i],
                number=transformed_numbers[i],
                moving=False
            )

        )

    # ---------- 卦宫 + 世应（关键新增） ----------

    key=(lower,upper)

    if key in HEXAGRAM_INFO:

        info=HEXAGRAM_INFO[key]

        palace=info["palace"]

        shi_pos=info["shi"]

        ying_pos=info["ying"]

        name=info["name"]

    else:

        # fallback（避免系统崩）
        palace="未知"

        shi_pos=3

        ying_pos=6

        name="未知卦"

    return {

        "original_lines":original_lines,
        "transformed_lines":transformed_lines,

        "lower":lower,
        "upper":upper,

        "lower_transformed":lower_t,
        "upper_transformed":upper_t,

        "numbers":lines,
        "transformed_numbers":transformed_numbers,

        # 新增
        "palace":palace,
        "shi_pos":shi_pos,
        "ying_pos":ying_pos,
        "hexagram_name":name

    }