def select_yongshen(divination, intent):
    """
    根据问题类型选择用神（改进版）
    - 用神基于问题对应六亲 + 世爻推导的六亲
    - 结合爻的状态、动爻、五爻等信息
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

    # 获取问题的目标六亲
    target_relative = mapping.get(intent, "妻财")

    # 找所有匹配的爻
    candidates = [l for l in divination.lines if l.relative == target_relative]

    # 如果没有匹配的六亲，用默认的世爻作为备用
    if not candidates:
        candidates = [divination.lines[2]]  # 默认选择世爻作为候选

    # 用神选择规则：
    # 1️⃣ 首选“得令/得地/旺”的爻
    for l in candidates:
        if l.state in ["旺", "得令"]:
            return l

    # 2️⃣ 选择动爻作为候选，如果没有“旺”的爻，则选择动爻
    moving_candidates = [l for l in candidates if l.moving]
    if moving_candidates:
        return moving_candidates[0]

    # 3️⃣ 若都不旺，则选择靠近中心的爻（五爻、四爻优先）
    candidates_sorted = sorted(candidates, key=lambda x: abs(x.pos - 4))
    return candidates_sorted[0]