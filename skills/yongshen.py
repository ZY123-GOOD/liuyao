def select_yongshen(divination, intent):
    """
    根据问题类型选择用神（改进版）
    - 用神基于问题对应六亲 + 世爻推导的六亲
    - 结合爻的状态、动爻、空亡等信息
    """
    # 问题类型对应六亲
    mapping = {
        "career": "官鬼",
        "exam": "父母",
        "wealth": "妻财",
        "investment": "妻财",
        "relationship": "妻财",
        "health": "官鬼",
        "food": "妻财"
    }

    target_relative = mapping.get(intent, "妻财")

    # 找所有匹配的爻，并排除空亡
    candidates = [l for l in divination.lines if l.relative == target_relative and l.pos not in divination.empty]

    # 如果没有匹配的六亲，用默认的世爻作为备用（排除空亡）
    if not candidates:
        shi = divination.lines[2]
        if shi.pos not in divination.empty:
            candidates = [shi]
        else:
            # 世爻也空亡，则选择其他非空爻
            candidates = [l for l in divination.lines if l.pos not in divination.empty]

    # 给每个候选爻评分
    scored = []
    for l in candidates:
        score = 0
        if l.state in ["旺", "得令"]:
            score += 2
        if l.moving:
            score += 1
        # 可在此加入冲、合、害影响，暂简单扣1分
        for conflict in divination.conflicts:
            if str(l.pos) in conflict["lines"]:
                score -= 1
        scored.append((score, l))

    # 选择分数最高的用神
    scored.sort(key=lambda x: (-x[0], abs(x[1].pos - 4)))  # 分数相同靠近中心优先
    return scored[0][1]