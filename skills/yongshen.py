# skills/yongshen.py

def select_yongshen(divination, intent):

    """
    根据问题类型选择用神

    intent:
    career
    wealth
    exam
    relationship
    health
    investment
    food

    返回：
    用神对应的 Line 对象
    """

    mapping = {

        "career":"官鬼",

        "exam":"父母",

        "wealth":"妻财",

        "investment":"妻财",

        "relationship":"妻财",

        "health":"官鬼",

        "food":"妻财"
    }

    target = mapping.get(intent,"妻财")

    # 找所有匹配六亲

    candidates=[]

    for l in divination.lines:

        if l.relative == target:

            candidates.append(l)

    # 如果没有

    if not candidates:

        return divination.lines[4]  # 默认五爻

    # 优先动爻

    moving=[l for l in candidates if l.moving]

    if moving:

        return moving[0]

    # 否则取位置最高

    return sorted(

        candidates,

        key=lambda x:x.pos,

        reverse=True

    )[0]