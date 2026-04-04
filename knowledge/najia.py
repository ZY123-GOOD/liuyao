# knowledge/najia.py

NAJIA={

"乾":["子","寅","辰"],

"兑":["巳","卯","丑"],

"离":["卯","丑","亥"],

"震":["子","寅","辰"],

"巽":["丑","亥","酉"],

"坎":["寅","辰","午"],

"艮":["寅","子","戌"],

"坤":["未","巳","卯"]

}

def get_branches(trigram):

    return NAJIA.get(trigram,[])
# knowledge/najia.py

# def get_branches(trigram):
#     """
#     获取指定卦象的地支
#     :param trigram: 三爻卦象，应该是 "乾", "坤", 等等
#     :return: 对应的地支列表，若无匹配则返回 None
#     """
#     branches = NAJIA.get(trigram)
#     if branches is None:
#         raise ValueError(f"未知的卦象：{trigram}，无法获取地支。请检查卦象输入是否正确。")
#     # 调试输出返回的地支
#     print(f"卦象：{trigram} 对应的地支：{branches}")
#     return branches