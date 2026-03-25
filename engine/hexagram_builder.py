# engine/hexagram_builder.py

from knowledge.trigrams import to_yinyang
from knowledge.trigrams import get_trigram

from knowledge.najia import get_branches

from engine.state import Line


def build(lines,day_element):

    """
    lines:

    [6,7,8,9...]

    """

    yin_yang=[

        to_yinyang(l)

        for l in lines

    ]

    lower=get_trigram(yin_yang[:3])

    upper=get_trigram(yin_yang[3:])

    branches=get_branches(lower)

    result=[]

    for i in range(6):

        moving=False

        if lines[i] in [6,9]:

            moving=True

        line=Line(

            i+1,

            branches[i],

            day_element,

            moving=moving

        )

        result.append(line)

    return result