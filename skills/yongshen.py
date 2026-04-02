# # skills/yongshen.py

# def select_yongshen(divination, intent):

#     """
#     根据问题类型选择用神

#     intent:
#     career
#     wealth
#     exam
#     relationship
#     health
#     investment
#     food

#     返回：
#     用神对应的 Line 对象
#     """

#     mapping = {

#         "career":"官鬼",

#         "exam":"父母",

#         "wealth":"妻财",

#         "investment":"妻财",

#         "relationship":"妻财",

#         "health":"官鬼",

#         "food":"妻财"
#     }

#     target = mapping.get(intent,"妻财")

#     # 找所有匹配六亲

#     candidates=[]

#     for l in divination.lines:

#         if l.relative == target:

#             candidates.append(l)

#     # 如果没有

#     if not candidates:

#         return divination.lines[4]  # 默认五爻

#     # 优先动爻

#     moving=[l for l in candidates if l.moving]

#     if moving:

#         return moving[0]

#     # 否则取位置最高

#     return sorted(

#         candidates,

#         key=lambda x:x.pos,

#         reverse=True

#     )[0]



def select_yongshen(divination, intent):
    """
    根据问题类型选择用神（改进版）
    - 用神基于问题对应六亲 + 世爻推导的六亲
    - 不再直接用动爻优先或默认五爻
    """
    # 问题类型对应六亲
    mapping = {
        "career":"官鬼",
        "exam":"父母",
        "wealth":"妻财",
        "investment":"妻财",
        "relationship":"妻财",
        "health":"官鬼",
        "food":"妻财"
    }

    target_relative = mapping.get(intent, "妻财")

    # 找所有匹配的爻
    candidates = [l for l in divination.lines if l.relative == target_relative]

    # 如果没有匹配，则选择世爻（初爻）为默认
    if not candidates:
        candidates = [divination.lines[0]]

    # 用神选择规则：
    # 1️⃣ 首选处于“得令/得地/旺”的爻
    for l in candidates:
        if l.state in ["旺", "得令"]:
            return l

    # 2️⃣ 若都不旺，则选择靠近中心的爻（五爻、四爻优先）
    candidates_sorted = sorted(candidates, key=lambda x: abs(x.pos-4))
    return candidates_sorted[0]