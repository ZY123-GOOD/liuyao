from openai import OpenAI
from config import QWEN_BASE_URL, QWEN_MODEL,API_key

import os
API_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_key, base_url=QWEN_BASE_URL)

def parse_intent(question):
    prompt = f"""
问题分类：
career, wealth, exam, relationship, health, investment
问题：{question}
只返回一个分类词
"""
    r = client.chat.completions.create(
        model=QWEN_MODEL,
        temperature=0,
        messages=[{"role":"user","content":prompt}]
    )
    return r.choices[0].message.content.strip()

def explain(rule_result):

    prompt=f"""
    你是专业六爻命理师。

    规则引擎已经完成推理，你的任务是：

    解释推理依据。

    不要重新判断吉凶。

    只解释为什么。

    规则推理结果：

    {rule_result}

    要求：

    说明：

    用神是谁

    为什么旺或弱

    哪些因素加分

    哪些因素减分

    写成专业断语。

    """
    r = client.chat.completions.create(
        model=QWEN_MODEL,
        temperature=0,
        messages=[{"role":"user","content":prompt}]
    )
    return r.choices[0].message.content


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

    要求：
    必须按规则推理解释，不要只描述数据。

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

    要求：

    必须按六爻真实推理顺序解释：

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