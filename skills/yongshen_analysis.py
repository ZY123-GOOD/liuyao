def analyze_yongshen(divination,line):

    score=0

    notes=[]

    # ----------------------
    # 五行关系表
    # ----------------------

    sheng={

    "木":"火",

    "火":"土",

    "土":"金",

    "金":"水",

    "水":"木"

    }

    ke={

    "木":"土",

    "土":"水",

    "水":"火",

    "火":"金",

    "金":"木"

    }

    def relation(a,b):

        if a==b:
            return "same"

        if sheng[a]==b:
            return "sheng"

        if sheng[b]==a:
            return "be_sheng"

        if ke[a]==b:
            return "ke"

        if ke[b]==a:
            return "be_ke"

        return "none"

    elem=line.element

    # ----------------------
    # 1 月令（最高权重）
    # ----------------------

    month=divination.month_element

    r=relation(month,elem)

    if r=="same":

        score+=3
        notes.append("得月令 +3")

    elif r=="sheng":

        score+=2
        notes.append("月生用神 +2")

    elif r=="be_sheng":

        score-=1
        notes.append("用神泄月 -1")

    elif r=="ke":

        score-=3
        notes.append("月克用神 -3")

    elif r=="be_ke":

        score-=1
        notes.append("用神克月 -1")

    # ----------------------
    # 2 日辰
    # ----------------------

    day=divination.day_element

    r=relation(day,elem)

    if r=="same":

        score+=2
        notes.append("得日辰 +2")

    elif r=="sheng":

        score+=1
        notes.append("日生用神 +1")

    elif r=="ke":

        score-=2
        notes.append("日克用神 -2")

    # ----------------------
    # 3 动爻
    # ----------------------

    if line.moving:

        score+=1

        notes.append("用神发动 +1")

    # ----------------------
    # 4 空亡
    # ----------------------

    if line.pos in divination.empty:

        score-=3

        notes.append("用神空亡 -3")

    # ----------------------
    # 5 冲合
    # ----------------------

    for c in divination.conflicts:

        if line.pos in c["lines"]:

            if c["type"]=="冲":

                score-=2

                notes.append("用神被冲 -2")

            elif c["type"]=="合":

                score+=1

                notes.append("用神被合 +1")

    # ----------------------
    # 6 六神（辅助）
    # ----------------------

    if line.liushen=="青龙":

        score+=0.5

        notes.append("青龙助吉 +0.5")

    elif line.liushen=="白虎":

        score-=0.5

        notes.append("白虎凶象 -0.5")

    elif line.liushen=="朱雀":

        notes.append("朱雀主口舌")

    elif line.liushen=="玄武":

        notes.append("玄武主暗事")

    # ----------------------
    # 7 世爻关系（关键）
    # ----------------------

    shi=divination.lines[2]   # 默认世爻第三爻

    r=relation(elem,shi.element)

    if r=="sheng":

        score+=1

        notes.append("用神生世 +1")

    elif r=="be_sheng":

        score+=0.5

        notes.append("世生用神 +0.5")

    elif r=="ke":

        score-=2

        notes.append("用神克世 -2")

    elif r=="be_ke":

        score-=2

        notes.append("世克用神 -2")

    # ----------------------
    # 8 其它爻影响（简化原神忌神）
    # ----------------------

    for l in divination.lines:

        if l.pos==line.pos:
            continue

        r=relation(l.element,elem)

        if r=="sheng":

            score+=0.5

            notes.append(f"{l.pos}爻生用神 +0.5")

        elif r=="ke":

            score-=0.5

            notes.append(f"{l.pos}爻克用神 -0.5")

    # ----------------------
    # 状态
    # ----------------------

    if score>=4:

        state="旺"

    elif score>=1:

        state="平"

    else:

        state="弱"

    return{

        "line":line,

        "score":round(score,2),

        "state":state,

        "notes":notes

    }