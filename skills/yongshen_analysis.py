def analyze_yongshen(divination, line):
    score = 0
    notes = []

    # 得月
    if line.element == divination.month_element:
        score += 2
        notes.append("用神得月旺 +2")
    # 得日
    if line.element == divination.day_element:
        score += 1
        notes.append("用神得日 +1")
    # 动爻
    if line.moving:
        score += 1
        notes.append("用神发动 +1")
    # 空亡
    if line.branch in divination.empty:
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
        notes.append("青龙吉 +1")
    elif line.liushen == "白虎":
        score -= 1
        notes.append("白虎凶 -1")

    if score is None:
        print("Warning: analyze_yongshen returned None score, defaulting to 0")
        score = 0  # 防止传 None 给 conclusion

    # 状态
    if score >= 2:
        state = "旺"
    elif score >= 0:
        state = "平"
    else:
        state = "弱"

    return {
        "line": line,
        "score": score,
        "state": state,
        "notes": notes
    }