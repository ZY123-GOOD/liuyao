# skills/conclusion.py
def conclusion(divination, line, score):
    """
    根据用神得分给出吉凶结论及置信度（专业版，匹配新版评分）
    """
    notes = []

    # ----------------------
    # 吉凶映射（与 analyze_yongshen 保持一致）
    # ----------------------
    if score >= 4:
        result = "吉"   # 旺
    elif score >= 1:
        result = "中"   # 平
    else:
        result = "凶"   # 弱

    # ----------------------
    # 动态置信度（与新版分值匹配）
    # ----------------------
    # 基础 0.55 + score*0.06，约束 0.2~0.9
    confidence = 0.55 + score * 0.06
    confidence = max(0.2, min(0.9, confidence))

    return {
        "result": result,
        "confidence": round(confidence, 2),
        "score": round(score, 2),
        "notes": notes
    }