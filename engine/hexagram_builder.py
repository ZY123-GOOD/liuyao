# engine/hexagram_builder.py

from knowledge.trigrams import to_yinyang
from knowledge.trigrams import get_trigram

from knowledge.najia import get_branches

from engine.state import Line

# engine/hexagram_builder.py

def build(lines, day_element):

    if len(lines) != 6:
        raise ValueError("六爻必须6个")

    yin_yang = [to_yinyang(l) for l in lines]

    lower = get_trigram(yin_yang[:3])
    upper = get_trigram(yin_yang[3:])

    # 正确纳甲
    lower_branches = get_branches(lower)
    upper_branches = get_branches(upper)

    if not lower_branches or not upper_branches:
        raise ValueError("纳甲失败")

    branches = lower_branches + upper_branches

    if len(branches) != 6:
        raise ValueError("纳甲必须6个")

    original_lines=[]

    for i in range(6):

        n=lines[i]

        original_lines.append(

            Line(
                pos=i+1,
                branch=branches[i],
                day_element=day_element,
                yin_yang=yin_yang[i],
                number=n,
                moving=(n in [6,9])
            )

        )

    # ---------- 变卦 ----------

    transformed_numbers=[]

    for n in lines:

        if n==6:
            transformed_numbers.append(7)

        elif n==9:
            transformed_numbers.append(8)

        else:
            transformed_numbers.append(n)

    transformed_yinyang=[to_yinyang(n) for n in transformed_numbers]

    lower_t=get_trigram(transformed_yinyang[:3])
    upper_t=get_trigram(transformed_yinyang[3:])

    branches_t=get_branches(lower_t)+get_branches(upper_t)

    transformed_lines=[]

    for i in range(6):

        transformed_lines.append(

            Line(
                pos=i+1,
                branch=branches_t[i],
                day_element=day_element,
                yin_yang=transformed_yinyang[i],
                number=transformed_numbers[i],
                moving=False
            )

        )

    return {

        "original_lines":original_lines,
        "transformed_lines":transformed_lines,

        "lower":lower,
        "upper":upper,

        "lower_transformed":lower_t,
        "upper_transformed":upper_t,

        "numbers":lines,
        "transformed_numbers":transformed_numbers

    }