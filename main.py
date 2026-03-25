from engine.divination import Divination
from engine.pipeline import run
from engine.coin import build_hexagram

# 用户自己投掷
user_coins = build_hexagram()
print("用户投掷结果:", user_coins)

# 初始化 Divination
d = Divination("这次投资能成功吗？", "male", coins=user_coins)
d.initialize()
print("Divination 状态：", d.summary())

# 调用 pipeline（含规则 + LLM 断语）
result = run(
    d.question,
    d.lines,
    d.month_element,
    d.day_element,
    d.gender,
    divination=d
)
print("断卦结果:", result)

