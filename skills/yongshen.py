def select_yongshen(divination, intent):
    """
    根据问题类型选择用神（增强版）
    支持人事、财务、健康、出行/天气
    评分规则：
      - 得令/旺 +2
      - 动爻 +1
      - 临凶神 -2
      - 被冲/害 -1~2
      - 静爻被动 -1
    """
    # 问题类型对应六亲
    mapping = {
        "career": "官鬼",
        "exam": "父母",
        "wealth": "妻财",
        "investment": "妻财",
        "relationship": "妻财",
        "health": "官鬼",
        "food": "妻财",
        "weather": "父母",
        "travel": "父母"   # 出行类问题也用父母爻
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
            candidates = [l for l in divination.lines if l.pos not in divination.empty]

    scored = []
    for l in candidates:
        score = 0
        # 爻状态评分
        if l.state in ["旺", "得令"]:
            score += 2
        if l.moving:
            score += 1
        # 冲、合、害扣分
        for conflict in divination.conflicts:
            if str(l.pos) in conflict.get("lines", []):
                score -= 1
        # 六神影响
        if l.liushen in ["白虎", "腾蛇", "玄武"]:
            score -= 2
        if l.liushen in ["朱雀"]:
            if intent in ["weather", "travel"]:
                score += 1  # 天气/出行遇朱雀利晴
        # 静爻被动扣分
        if not l.moving:
            score -= 1

        scored.append((score, l))

    # 按分数排序，分数相同优先靠近中心爻
    scored.sort(key=lambda x: (-x[0], abs(x[1].pos - 4)))
    return scored[0][1]