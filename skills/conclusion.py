# skills/conclusion.py

def conclusion(divination, line, score):

    notes=[]

    # 动爻

    if line.moving:

        score+=1

        notes.append("用神动 +1")

    # 空亡

    if line.branch in divination.empty:

        score-=2

        notes.append("用神空亡 -2")

    # 冲合

    for c in divination.conflicts:

        if line.pos in c["lines"]:

            if c["type"]=="冲":

                score-=1

                notes.append("用神被冲 -1")

            elif c["type"]=="合":

                score+=1

                notes.append("用神被合 +1")

    # 六神

    if line.liushen=="青龙":

        score+=1

        notes.append("青龙助吉 +1")

    if line.liushen=="白虎":

        score-=1

        notes.append("白虎减分 -1")

    # 最终判断

    if score>=4:

        result="吉"

        confidence=0.75

    elif score>=1:

        result="中"

        confidence=0.55

    else:

        result="凶"

        confidence=0.35

    return {

        "result":result,

        "confidence":confidence,

        "score":score,

        "notes":notes
    }