# # skills/yongshen_analysis.py
# # 专业版 analyze_yongshen，支持五行生克、世应、忌神、卦意趋势评分
# # 分数重新平衡，吉凶对称，避免偏向凶

# def analyze_yongshen(divination, line):
#     """
#     分析用神的得分、状态及详细备注（专业版）
#     divination: Divination对象
#     line: Line对象（用神爻）
#     返回: dict, 包含评分、状态、备注
#     """

#     score = 0
#     notes = []

#     # ----------------------
#     # 五行关系表
#     # ----------------------
#     sheng = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
#     ke = {"木":"土","土":"水","水":"火","火":"金","金":"木"}

#     def relation(a,b):
#         if a==b:
#             return "same"
#         if sheng[a]==b:
#             return "sheng"
#         if sheng[b]==a:
#             return "be_sheng"
#         if ke[a]==b:
#             return "ke"
#         if ke[b]==a:
#             return "be_ke"
#         return "none"

#     elem = line.element

#     # ----------------------
#     # 1️⃣ 月令
#     # ----------------------
#     month = divination.month_element
#     r = relation(month, elem)
#     if r == "same":
#         score += 3
#         notes.append("得月令 +3")
#     elif r == "sheng":
#         score += 2
#         notes.append("月生用神 +2")
#     elif r == "be_sheng":
#         score -= 1
#         notes.append("用神泄月 -1")
#     elif r == "ke":
#         score -= 2  # 调整从 -3 → -2
#         notes.append("月克用神 -2")
#     elif r == "be_ke":
#         score -= 0.5  # 调整从 -1 → -0.5
#         notes.append("用神克月 -0.5")

#     # ----------------------
#     # 2️⃣ 日辰
#     # ----------------------
#     day = divination.day_element
#     r = relation(day, elem)
#     if r == "same":
#         score += 2
#         notes.append("得日辰 +2")
#     elif r == "sheng":
#         score += 1
#         notes.append("日生用神 +1")
#     elif r == "be_sheng":
#         score -= 0.5
#         notes.append("世生日辰 -0.5")
#     elif r == "ke":
#         score -= 1  # 调整从 -2 → -1
#         notes.append("日克用神 -1")
#     elif r == "be_ke":
#         score -= 0.5  # 调整从 -1 → -0.5
#         notes.append("用神克日 -0.5")

#     # ----------------------
#     # 3️⃣ 动爻
#     # ----------------------
#     if line.moving:
#         score += 1  # 调整从 +0.5 → +1
#         notes.append("用神发动 +1")

#     # ----------------------
#     # 4️⃣ 空亡
#     # ----------------------
#     if line.pos in divination.empty:
#         score -= 2  # 调整从 -3 → -2
#         notes.append("用神空亡 -2")

#     # ----------------------
#     # 5️⃣ 冲合
#     # ----------------------
#     for c in divination.conflicts:
#         if line.pos in c["lines"]:
#             if c["type"] == "冲":
#                 score -= 1.5  # 调整从 -2 → -1.5
#                 notes.append("用神被冲 -1.5")
#             elif c["type"] == "合":
#                 score += 1.5  # 调整从 +1 → +1.5
#                 notes.append("用神被合 +1.5")

#     # ----------------------
#     # 6️⃣ 六神（辅助）
#     # ----------------------
#     if line.liushen == "青龙":
#         score += 0.5
#         notes.append("青龙助吉 +0.5")
#     elif line.liushen == "白虎":
#         score -= 0.5
#         notes.append("白虎凶象 -0.5")
#     elif line.liushen == "朱雀":
#         notes.append("朱雀主口舌")
#     elif line.liushen == "玄武":
#         notes.append("玄武主隐情")

#     # ----------------------
#     # 7️⃣ 世应关系（关键）
#     # ----------------------
#     shi = divination.lines[2]  # 默认三爻为世
#     r = relation(elem, shi.element)
#     if r == "sheng":
#         score += 1.5  # 调整从 +1 → +1.5
#         notes.append("用神生世 +1.5")
#     elif r == "be_sheng":
#         score += 1  # 调整从 +0.5 → +1
#         notes.append("世生用神 +1")
#     elif r == "ke":
#         score -= 1.5  # 调整从 -2 → -1.5
#         notes.append("用神克世 -1.5")
#     elif r == "be_ke":
#         score -= 1.5  # 调整从 -2 → -1.5
#         notes.append("世克用神 -1.5")

#     # ----------------------
#     # 8️⃣ 其它爻生克
#     # ----------------------
#     for l in divination.lines:
#         if l.pos == line.pos:
#             continue
#         r = relation(l.element, elem)
#         if r == "sheng":
#             score += 0.5
#             notes.append(f"{l.pos}爻生用神 +0.5")
#         elif r == "ke":
#             score -= 0.5  # 调整从 -0.7 → -0.5
#             notes.append(f"{l.pos}爻克用神 -0.5")

#     # ----------------------
#     # 9️⃣ 动爻结构风险
#     # ----------------------
#     moving_count = sum(1 for l in divination.lines if l.moving)
#     if moving_count >= 4:
#         score -= 0.5  # 调整从 -1 → -0.5
#         notes.append("动爻过多局势不稳 -0.5")
#     if moving_count == 6:
#         score -= 1  # 调整从 -2 → -1
#         notes.append("六爻全动大变 -1")

#     # ----------------------
#     # 🔑 10 忌神专项扣分
#     # ----------------------
#     if line.relative == "官鬼":
#         child_lines = [l for l in divination.lines if l.relative=="子孙"]
#         moving_child = [l for l in child_lines if l.moving]
#         if len(child_lines) >= 2:
#             score -= 1.5  # 调整从 -2 → -1.5
#             notes.append("子孙多现克官（忌神结构） -1.5")
#         if len(moving_child) >= 1:
#             score -= 1
#             notes.append("子孙动克官（大忌） -1")
#     if line.relative == "妻财":
#         brother = [l for l in divination.lines if l.relative=="兄弟"]
#         moving_brother = [l for l in brother if l.moving]
#         if len(brother) >= 2:
#             score -= 0.8  # 调整从 -1 → -0.8
#             notes.append("兄弟多夺财 -0.8")
#         if len(moving_brother) >= 1:
#             score -= 0.5
#             notes.append("兄弟动夺财 -0.5")

#     # ----------------------
#     # 11️⃣ 用神不动减分
#     # ----------------------
#     if not line.moving:
#         score -= 0.5  # 调整从 -1 → -0.5
#         notes.append("用神不动（事情无推动） -0.5")

#     # ----------------------
#     # 12️⃣ 卦意趋势加分/减分
#     # ----------------------
#     if hasattr(divination,"main_gua") and divination.main_gua in ["否","困"]:
#         score -= 1
#         notes.append(f"{divination.main_gua}卦闭塞 -1")

#     # ----------------------
#     # 状态判断
#     # ----------------------
#     if score >= 5:
#         state = "旺"
#     elif score >= 1:
#         state = "平"
#     else:
#         state = "弱"

#     return {
#         "line": line,
#         "score": round(score, 2),
#         "state": state,
#         "notes": notes
#     }


# def analyze_yongshen(divination, line):

#     score = 0
#     notes = []

#     sheng = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
#     ke = {"木":"土","土":"水","水":"火","火":"金","金":"木"}

#     def relation(a,b):

#         if a==b:
#             return "same"

#         if sheng[a]==b:
#             return "sheng"

#         if sheng[b]==a:
#             return "be_sheng"

#         if ke[a]==b:
#             return "ke"

#         if ke[b]==a:
#             return "be_ke"

#         return "none"

#     elem = line.element

#     # ----------------------
#     # 1 月令（最高权重）
#     # ----------------------

#     month = divination.month_element

#     r = relation(month,elem)

#     if r=="same":
#         score+=3
#         notes.append("得月令 +3")

#     elif r=="sheng":
#         score+=2
#         notes.append("月生用神 +2")

#     elif r=="be_sheng":
#         score-=1
#         notes.append("用神泄月 -1")

#     elif r=="ke":
#         score-=2
#         notes.append("月克用神 -2")

#     elif r=="be_ke":
#         score-=0.5
#         notes.append("用神克月 -0.5")

#     # ----------------------
#     # 2 日辰
#     # ----------------------

#     day = divination.day_element

#     r = relation(day,elem)

#     if r=="same":

#         score+=2
#         notes.append("得日辰 +2")

#     elif r=="sheng":

#         score+=1
#         notes.append("日生用神 +1")

#     elif r=="be_sheng":

#         score-=0.5
#         notes.append("用神泄日 -0.5")

#     elif r=="ke":

#         score-=1
#         notes.append("日克用神 -1")

#     elif r=="be_ke":

#         score-=0.5
#         notes.append("用神克日 -0.5")

#     # ----------------------
#     # 3 用神发动
#     # ----------------------

#     if line.moving:

#         score+=1.5
#         notes.append("用神发动 +1.5")

#     # ----------------------
#     # 4 空亡（降低权重）
#     # ----------------------

#     if line.pos in divination.empty:

#         score-=1.5
#         notes.append("用神空亡 -1.5")

#     # ----------------------
#     # 5 冲合
#     # ----------------------

#     for c in divination.conflicts:

#         if line.pos in c["lines"]:

#             if c["type"]=="冲":

#                 score-=1.2
#                 notes.append("用神被冲 -1.2")

#             elif c["type"]=="合":

#                 score+=1.2
#                 notes.append("用神被合 +1.2")

#     # ----------------------
#     # 6 六神辅助（小权重）
#     # ----------------------

#     if line.liushen=="青龙":

#         score+=0.5
#         notes.append("青龙助吉 +0.5")

#     elif line.liushen=="白虎":

#         score-=0.5
#         notes.append("白虎凶象 -0.5")

#     # ----------------------
#     # 7 世应关系（关键结构）
#     # ----------------------

#     shi = divination.lines[2]

#     r = relation(elem,shi.element)

#     if r=="sheng":

#         score+=1.5
#         notes.append("用神生世 +1.5")

#     elif r=="be_sheng":

#         score+=1
#         notes.append("世生用神 +1")

#     elif r=="ke":

#         score-=1.5
#         notes.append("用神克世 -1.5")

#     elif r=="be_ke":

#         score-=1.5
#         notes.append("世克用神 -1.5")

#     # ----------------------
#     # 8 其它爻净生克（核心优化）
#     # ----------------------

#     sheng_count=0
#     ke_count=0

#     for l in divination.lines:

#         if l.pos==line.pos:
#             continue

#         r = relation(l.element,elem)

#         if r=="sheng":

#             sheng_count+=1

#         elif r=="ke":

#             ke_count+=1

#     net = (sheng_count-ke_count)*0.4

#     score+=net

#     if net>0:

#         notes.append(f"他爻生助 {sheng_count} - 克 {ke_count} +{round(net,2)}")

#     elif net<0:

#         notes.append(f"他爻克制 {ke_count} - 生 {sheng_count} {round(net,2)}")

#     # ----------------------
#     # 9 动爻结构
#     # ----------------------

#     moving_count=sum(1 for l in divination.lines if l.moving)

#     if moving_count>=4:

#         score-=0.5
#         notes.append("动爻多局势乱 -0.5")

#     if moving_count==6:

#         score-=1
#         notes.append("六爻全动大变 -1")

#     # ----------------------
#     # 10 忌神结构
#     # ----------------------

#     if line.relative=="官鬼":

#         child=[l for l in divination.lines if l.relative=="子孙"]

#         moving_child=[l for l in child if l.moving]

#         if len(child)>=2:

#             score-=1.2
#             notes.append("子孙多克官 -1.2")

#         if len(moving_child)>=1:

#             score-=0.8
#             notes.append("子孙发动克官 -0.8")

#     if line.relative=="妻财":

#         bro=[l for l in divination.lines if l.relative=="兄弟"]

#         moving_bro=[l for l in bro if l.moving]

#         if len(bro)>=2:

#             score-=0.8
#             notes.append("兄弟多夺财 -0.8")

#         if len(moving_bro)>=1:

#             score-=0.5
#             notes.append("兄弟动夺财 -0.5")

#     # ----------------------
#     # 11 卦意趋势
#     # ----------------------

#     if hasattr(divination,"main_gua"):

#         if divination.main_gua in ["否","困"]:

#             score-=1
#             notes.append("卦意闭塞 -1")

#         if divination.main_gua in ["泰","升"]:

#             score+=1
#             notes.append("卦意上升 +1")

#     # ----------------------
#     # 状态判断（更合理区间）
#     # ----------------------

#     if score>=4:

#         state="旺"

#     elif score>=0:

#         state="平"

#     else:

#         state="弱"

#     return {

#         "line":line,

#         "score":round(score,2),

#         "state":state,

#         "notes":notes
#     }

def analyze_yongshen(divination, line):
    score = 0
    notes = []

    sheng = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
    ke = {"木":"土","土":"水","水":"火","火":"金","金":"木"}

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

    elem = line.element

    # ----------------------
    # 1 月令（最高权重）
    # ----------------------
    month = divination.month_element
    r = relation(month, elem)
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
        score-=1.5  # 调低负分权重
        notes.append("月克用神 -1.5")
    elif r=="be_ke":
        score-=0.5
        notes.append("用神克月 -0.5")

    # ----------------------
    # 2 日辰
    # ----------------------
    day = divination.day_element
    r = relation(day, elem)
    if r=="same":
        score+=2
        notes.append("得日辰 +2")
    elif r=="sheng":
        score+=1
        notes.append("日生用神 +1")
    elif r=="be_sheng":
        score-=0.5
        notes.append("用神泄日 -0.5")
    elif r=="ke":
        score-=1
        notes.append("日克用神 -1")
    elif r=="be_ke":
        score-=0.5
        notes.append("用神克日 -0.5")

    # ----------------------
    # 3 用神发动
    # ----------------------
    if line.moving:
        score+=1.5
        notes.append("用神发动 +1.5")

    # ----------------------
    # 4 空亡
    # ----------------------
    if line.pos in divination.empty:
        score-=1
        notes.append("用神空亡 -1")  # 降低负分

    # ----------------------
    # 5 冲合
    # ----------------------
    for c in divination.conflicts:
        if line.pos in c["lines"]:
            if c["type"]=="冲":
                score-=1
                notes.append("用神被冲 -1")
            elif c["type"]=="合":
                score+=1
                notes.append("用神被合 +1")

    # ----------------------
    # 6 六神辅助
    # ----------------------
    if line.liushen=="青龙":
        score+=0.5
        notes.append("青龙助吉 +0.5")
    elif line.liushen=="白虎":
        score-=0.5
        notes.append("白虎凶象 -0.5")

    # ----------------------
    # 7 世应关系
    # ----------------------
    shi = divination.lines[2]
    r = relation(elem, shi.element)
    if r=="sheng":
        score+=1.5
        notes.append("用神生世 +1.5")
    elif r=="be_sheng":
        score+=1
        notes.append("世生用神 +1")
    elif r=="ke":
        score-=1.2
        notes.append("用神克世 -1.2")
    elif r=="be_ke":
        score-=1.2
        notes.append("世克用神 -1.2")

    # ----------------------
    # 8 其它爻净生克
    # ----------------------
    sheng_count=0
    ke_count=0
    for l in divination.lines:
        if l.pos==line.pos:
            continue
        r = relation(l.element, elem)
        if r=="sheng":
            sheng_count+=1
        elif r=="ke":
            ke_count+=1
    net = (sheng_count-ke_count)*0.4
    score += net
    if net>0:
        notes.append(f"他爻生助 {sheng_count} - 克 {ke_count} +{round(net,2)}")
    elif net<0:
        notes.append(f"他爻克制 {ke_count} - 生 {sheng_count} {round(net,2)}")

    # ----------------------
    # 9 动爻结构
    # ----------------------
    moving_count=sum(1 for l in divination.lines if l.moving)
    if moving_count>=4:
        score-=0.5
        notes.append("动爻多局势乱 -0.5")
    if moving_count==6:
        score-=0.8
        notes.append("六爻全动大变 -0.8")

    # ----------------------
    # 10 忌神结构
    # ----------------------
    if line.relative=="官鬼":
        child=[l for l in divination.lines if l.relative=="子孙"]
        moving_child=[l for l in child if l.moving]
        if len(child)>=2:
            score-=1
            notes.append("子孙多克官 -1")
        if len(moving_child)>=1:
            score-=0.5
            notes.append("子孙发动克官 -0.5")
    if line.relative=="妻财":
        bro=[l for l in divination.lines if l.relative=="兄弟"]
        moving_bro=[l for l in bro if l.moving]
        if len(bro)>=2:
            score-=0.5
            notes.append("兄弟多夺财 -0.5")
        if len(moving_bro)>=1:
            score-=0.3
            notes.append("兄弟动夺财 -0.3")

    # ----------------------
    # 11 卦意趋势加分
    # ----------------------
    trend_bonus = 0
    if hasattr(divination,"main_gua"):
        if divination.main_gua in ["泰","升","大有","益"]:
            trend_bonus += 1.5
            notes.append(f"{divination.main_gua}卦趋势吉 +1.5")
        if divination.main_gua in ["否","困"]:
            trend_bonus -= 1
            notes.append(f"{divination.main_gua}卦闭塞 -1")
    score += trend_bonus

    # ----------------------
    # 状态判断（更职业级）
    # ----------------------
    if score >= 5:
        state = "旺"
    elif score >= 2:
        state = "中上"
    elif score >= 0:
        state = "平"
    else:
        state = "弱"

    return {
        "line": line,
        "score": round(score,2),
        "state": state,
        "notes": notes
    }