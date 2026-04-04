# engine/hexagram_builder.py

from knowledge.trigrams import to_yinyang
from knowledge.trigrams import get_trigram

from knowledge.najia import get_branches

from engine.state import Line

# engine/hexagram_builder.py

def build(lines, day_element):
    """
    构建六爻结构
    """
    if len(lines) != 6:
        raise ValueError("六爻必须6个")

    # ---------- 阴阳转换 ----------
    yin_yang = [to_yinyang(l) for l in lines]

    # ---------- 上下卦 ----------
    lower = get_trigram(yin_yang[:3])
    upper = get_trigram(yin_yang[3:])

    # 打印生成的上下卦，查看返回值是否正确
    print(f"生成的下卦：{lower}, 上卦：{upper}")

    # ---------- 纳甲地支 ----------
    branches = get_branches(lower)
    
    # 打印获取的地支数量和内容
    print(f"获取的地支：{branches}, 地支数量：{len(branches)}")

    # 必须6个
    if len(branches) != 6:
        raise ValueError(f"纳甲必须返回6个地支，当前返回地支数量：{len(branches)}，地支内容：{branches}")

    # ---------- 构建本卦 ----------
    original_lines = []
    for i in range(6):
        number = lines[i]
        moving = False
        if number == 6 or number == 9:
            moving = True
        line = Line(
            pos=i+1,
            branch=branches[i],
            day_element=day_element,
            yin_yang=yin_yang[i],
            number=number,
            moving=moving
        )
        original_lines.append(line)

    # ---------- 生成变卦 ----------
    transformed_numbers = []
    for n in lines:
        if n == 6:
            transformed_numbers.append(7)
        elif n == 9:
            transformed_numbers.append(8)
        else:
            transformed_numbers.append(n)

    transformed_yinyang = [to_yinyang(n) for n in transformed_numbers]

    lower_t = get_trigram(transformed_yinyang[:3])
    upper_t = get_trigram(transformed_yinyang[3:])
    branches_t = get_branches(lower_t)
    
    # 打印变卦地支
    print(f"变卦地支：{branches_t}, 地支数量：{len(branches_t)}")

    transformed_lines = []
    for i in range(6):
        line = Line(
            pos=i+1,
            branch=branches_t[i],
            day_element=day_element,
            yin_yang=transformed_yinyang[i],
            number=transformed_numbers[i],
            moving=False
        )
        transformed_lines.append(line)

    # ---------- 返回结构 ----------
    return {
        "original_lines": original_lines,
        "transformed_lines": transformed_lines,
        "lower": lower,
        "upper": upper,
        "lower_transformed": lower_t,
        "upper_transformed": upper_t,
        "numbers": lines,
        "transformed_numbers": transformed_numbers
    }