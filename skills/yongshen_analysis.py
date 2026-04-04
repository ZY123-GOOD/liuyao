def analyze_yongshen(divination, line):
    """
    分析用神的得分、状态及相关备注。
    divination: Divination 对象
    line: Line 对象（即用神爻）
    返回：包含评分、状态及备注的字典
    """
    score = 0
    notes = []

    # 1️⃣ 用神得月（根据月令得分）
    if line.element == divination.month_element:
        score += 2
        notes.append("用神得月旺 +2")
    
    # 2️⃣ 用神得日（根据日辰得分）
    if line.element == divination.day_element:
        score += 1
        notes.append("用神得日 +1")

    # 3️⃣ 动爻（用神爻是否动）
    if line.moving:
        score += 1
        notes.append("用神发动 +1")

    # 4️⃣ 空亡（用神是否落空亡）
    if line.branch in divination.empty:
        score -= 2
        notes.append("用神空亡 -2")

    # 5️⃣ 冲合（用神是否被冲或合）
    for c in divination.conflicts:
        if line.pos in c["lines"]:
            if c["type"] == "冲":
                score -= 1
                notes.append("用神被冲 -1")
            elif c["type"] == "合":
                score += 1
                notes.append("用神被合 +1")

    # 6️⃣ 六神（用神的六神状态）
    if line.liushen == "青龙":
        score += 1
        notes.append("青龙吉 +1")
    elif line.liushen == "白虎":
        score -= 1
        notes.append("白虎凶 -1")

    # 7️⃣ 状态判断（根据得分计算用神状态）
    if score >= 3:
        state = "旺"  # 用神非常有力，能够带来成功
    elif score >= 1:
        state = "平"  # 用神正常，维持平衡
    else:
        state = "弱"  # 用神疲弱，可能存在阻碍

    return {
        "line": line,
        "score": score,
        "state": state,
        "notes": notes
    }