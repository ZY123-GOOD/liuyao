from openai import OpenAI
from config import QWEN_BASE_URL, QWEN_MODEL

import os
API_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_key, base_url=QWEN_BASE_URL)

def parse_intent(question):
    """
    问题分类增强版
    支持人事类、财务类、健康、考试，以及天气/出行类问题
    """
    categories = [
        "career",       # 职业、升迁、工作
        "wealth",       # 财富、财务
        "exam",         # 考试、学业
        "relationship", # 感情、人际
        "health",       # 健康、医疗
        "investment",   # 投资理财
        "travel",       # 出行、旅游
        "weather"       # 天气、气候
    ]
    
    prompt = f"""
问题分类：
{', '.join(categories)}
请根据问题内容选择最合适的分类，只返回一个分类词，不要解释。
问题：{question}
"""
    r = client.chat.completions.create(
        model=QWEN_MODEL,
        temperature=0,
        messages=[{"role":"user","content":prompt}]
    )
    intent = r.choices[0].message.content.strip()
    
    # 如果返回不在分类内，默认 "wealth"
    if intent not in categories:
        intent = "wealth"
    return intent


def explain_step_by_step(

    divination,

    rule_result,

    yongshen,

    yongshen_analysis

):
    """
    divination: Divination 对象
    rule_result: conclusion()结果
    yongshen: 用神信息
    yongshen_analysis: 用神旺衰分析
    """

    prompt = f"""
            你是专业六爻命理师，请严格按照六爻断卦逻辑，逐步解释推算过程。

            用户问题：
            {divination.question}

            【起卦数据】
            铜钱：{divination.original}
            动爻：{divination.moving}
            本卦：{divination.lines}
            变卦：{divination.transformed}

            【时间】
            日支：{divination.day_branch} 日五行：{divination.day_element}
            月支：{divination.month_branch} 月五行：{divination.month_element}

            【六神】{divination.liu_shen}
            【空亡】{divination.empty}
            【冲合】{divination.conflicts}
            【用神】{yongshen}
            【用神旺衰】{yongshen_analysis}
            【规则推理结果】{rule_result}

            要求：
            1. 按编号顺序输出，每一步用 ### 标题，内容用段落说明。
            2. 不使用箭头或表格，全部用中文自然文字。
            3. 用神分析必须引用具体爻位、爻象、五行、六亲、六神状态，说明得分来源。
            4. 变卦分析必须解释原卦→变卦的趋势和可能结果。
            5. 输出最终结论格式：
            - 结果：吉/中/凶
            - 原因：用神状态总结
            - 趋势：事情发展判断
    """
    


    prompt = f"""
    你是专业六爻命理师，请严格按照六爻断卦逻辑，逐步解释推算过程。

    用户问题：
    {divination.question}

    【起卦数据】

    铜钱：
    {divination.original}
    动爻：
    {divination.moving}
    本卦：
    {divination.lines}
    变卦：
    {divination.transformed}

    【时间】
    日支：
    {divination.day_branch}
    日五行：
    {divination.day_element}
    月支：
    {divination.month_branch}
    月五行：
    {divination.month_element}

    【六神】
    {divination.liu_shen}

    【空亡】
    {divination.empty}
    【冲合】

    {divination.conflicts}
    【用神】

    {yongshen}
    【用神旺衰】

    {yongshen_analysis}
    【规则推理结果】

    {rule_result}
    要求：根据上述信息，必须按六爻真实推理顺序解释：
    ### 1 记录时间
    说明月建日辰对五行影响

    ### 2 起卦
    解释铜钱阴阳意义

    ### 3 本卦生成
    说明上下卦五行

    ### 4 动爻
    解释动爻代表变化

    ### 5 变卦
    说明趋势变化

    ### 6 干支
    说明日月五行关系

    ### 7 六亲
    说明各爻六亲

    ### 8 六神
    说明六神象意

    ### 9 用神分析（重点）
    必须解释：
    用神是否旺  
    是否受克  
    是否空亡  
    是否被冲  
    是否发动  

    ### 10 断神分析（关键推理）

    必须解释：

    为什么判吉或凶

    例如：

    用神旺 → 加分

    被冲 → 减分

    发动 → 加分

    空亡 → 减分

    必须体现规则推理逻辑。

    ### 11 最终结论

    必须输出：

    结果：
    吉 / 中 / 凶

    原因：
    用神状态总结

    趋势：
    事情发展判断

    不要使用箭头符号。
    用纯Markdown。
    """
    
    
    
    r = client.chat.completions.create(
        model=QWEN_MODEL,
        temperature=0,
        messages=[{"role":"user","content":prompt}]
    )
    return r.choices[0].message.content