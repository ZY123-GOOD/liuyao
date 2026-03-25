# pipeline/pipeline.py

from llm.qwen_client import parse_intent, explain_step_by_step

from skills.yongshen import select_yongshen

from skills.yongshen_analysis import analyze_yongshen

from skills.conclusion import conclusion


def run(divination):

    """
    六爻推理主流程

    divination:
    已完成 initialize() 的 Divination 对象

    返回：

    UI需要的数据结构
    """

    # ----------------------
    # 1 Intent解析
    # ----------------------

    intent = parse_intent(

        divination.question

    )


    # ----------------------
    # 2 选择用神
    # ----------------------

    yongshen_line = select_yongshen(

        divination,

        intent

    )


    # ----------------------
    # 3 用神分析
    # ----------------------

    yongshen_result = analyze_yongshen(

        divination,

        yongshen_line

    )


    # ----------------------
    # 4 最终结论
    # ----------------------

    base_result = conclusion(

        divination,

        yongshen_line,

        yongshen_result["score"]

    )


    # ----------------------
    # 5 合并推理数据
    # ----------------------

    rule_result = {

        "result":base_result["result"],

        "confidence":base_result["confidence"],

        "score":base_result["score"],

        "intent":intent,

        "yongshen":{

            "pos":yongshen_line.pos,

            "relative":yongshen_line.relative,

            "element":yongshen_line.element,

            "moving":yongshen_line.moving,

            "liushen":yongshen_line.liushen,

            "branch":yongshen_line.branch,

            "state":yongshen_result["state"]

        },

        "notes":

        yongshen_result["notes"]

        +

        base_result["notes"]

    }


    # ----------------------
    # 6 LLM逐步解释
    # ----------------------

    explanation = explain_step_by_step(

        divination,

        rule_result,
        
        yongshen_line,

        yongshen_result

    )


    # ----------------------
    # 7 返回UI数据
    # ----------------------

    return {

        "base_result":rule_result,

        "text":explanation,

        "intent":intent

    }