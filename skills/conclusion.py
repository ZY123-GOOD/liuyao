def conclusion(divination, line, score):

    notes = []

    if score is None:
        score = 0

    # 动爻
    if line.moving:
        score += 1
        notes.append("用神动 +1")

    # 空亡
    if line.state == "空亡":
        score -= 2
        notes.append("用神空亡 -2")

    # 冲合
    for c in divination.conflicts:

        if line.pos in c["lines"]:

            if c["type"] == "冲":

                score -= 1
                notes.append("用神被冲 -1")

            elif c["type"] == "合":

                score += 1
                notes.append("用神被合 +1")

    # 六神
    if line.liushen == "青龙":

        score += 1
        notes.append("青龙助吉 +1")

    elif line.liushen == "白虎":

        score -= 1
        notes.append("白虎减分 -1")

    elif line.liushen == "朱雀":

        notes.append("朱雀主口舌")

    elif line.liushen == "玄武":

        notes.append("玄武主隐情")

    # -------- 吉凶判断 --------

    if score >= 2:

        result = "吉"

    elif score >= -1:

        result = "中"

    else:

        result = "凶"

    # -------- 动态置信度 --------

    confidence = 0.5 + score * 0.07

    confidence = max(0.15, min(0.95, confidence))

    return {

        "result": result,

        "confidence": round(confidence,2),

        "score": score,

        "notes": notes

    }