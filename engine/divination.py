# skills/divination.py

from datetime import datetime
from engine.coin import build_hexagram
from engine.hexagram_builder import build
from knowledge.calendar import get_day_branch, get_month_branch
from knowledge.branches import get_element
from knowledge.liuqin import get_relative

LIU_SHEN_ORDER = ["青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武"]

EMPTY_BRANCH = {
    "甲子": ["戌", "亥"], "乙丑": ["戌", "亥"], "丙寅": ["子", "丑"],
    "丁卯": ["子", "丑"], "戊辰": ["寅", "卯"], "己巳": ["寅", "卯"],
    "庚午": ["辰", "巳"], "辛未": ["辰", "巳"], "壬申": ["午", "未"],
    "癸酉": ["午", "未"], "甲戌": ["申", "酉"], "乙亥": ["申", "酉"]
}

CLASH = {("子", "午"): "冲", ("午", "子"): "冲", ("寅", "申"): "冲", ("申", "寅"): "冲",
         ("巳", "亥"): "冲", ("亥", "巳"): "冲", ("卯", "酉"): "冲", ("酉", "卯"): "冲"}

COMBINE = {("子", "丑"): "合", ("丑", "子"): "合", ("寅", "亥"): "合", ("亥", "寅"): "合"}


class Divination:
    def __init__(self, question, gender=None, dt=None, coins=None):
        self.question = question
        self.gender = gender
        self.datetime = dt if dt else datetime.now()
        self.coins = coins

        # 卦爻信息
        self.original = self.transformed = None
        self.lines = []
        self.moving = []

        # 时间与五行
        self.day_branch = self.month_branch = None
        self.day_element = self.month_element = None

        # 六神/空亡/冲合
        self.liu_shen = [None] * 6
        self.empty = []
        self.conflicts = []

        # 卦名/世应/卦宫
        self.base_name = None
        self.trans_name = None
        self.hexagram_name = None
        self.main_gua = None  # ✅ 关键属性，配合 analyze_yongshen
        self.palace = None
        self.shi_pos = 3
        self.ying_pos = 6
        self.shi_yao = None

    # -------------------- 卦生成 --------------------
    def cast(self):
        """生成原始卦象"""
        self.original = self.coins if self.coins else build_hexagram()
        self.moving = [i + 1 for i, v in enumerate(self.original) if v in [6, 9]]
        self.transformed = self.transform()

    def transform(self):
        """转换卦象，将6和9转换为7和8"""
        return [7 if l == 6 else 8 if l == 9 else l for l in self.original]

    # -------------------- 时间/五行 --------------------
    def calc_time(self):
        """计算日支、月支及五行"""
        self.day_branch = get_day_branch(self.datetime)
        self.month_branch = get_month_branch(self.datetime)
        self.day_element = get_element(self.day_branch)
        self.month_element = get_element(self.month_branch)

    # -------------------- 爻生成/六亲/状态 --------------------
    def build_lines(self):
        """根据原始卦象和日主构建爻对象"""
        result = build(self.original, self.day_element)
        self.lines = result["original_lines"]
        self.palace = result.get("palace", "未知")
        self.shi_pos = result.get("shi_pos", 3)
        self.ying_pos = result.get("ying_pos", 6)
        self.hexagram_name = result.get("hexagram_name", "未知卦")
        self.main_gua = result.get("hexagram_name", "未知卦")  # ✅ 添加main_gua

        for i, l in enumerate(self.lines):
            l.number = self.original[i]
            l.state = "平"

        self.shi_yao = self.lines[self.shi_pos - 1]

    def enrich_lines(self):
        """为爻填充五行、六亲及动爻状态"""
        for l in self.lines:
            l.set_element(get_element(l.branch))
            l.set_relative(get_relative(self.day_element, l.element))
            l.moving = (l.pos in self.moving)

    def mark_shi_ying(self):
        """标记世爻和应爻"""
        for l in self.lines:
            l.shi = False
            l.ying = False
        self.lines[self.shi_pos - 1].shi = True
        self.lines[self.ying_pos - 1].ying = True

    def assign_liu_shen(self):
        """为每个爻指定六神"""
        for i, l in enumerate(self.lines):
            l.liushen = LIU_SHEN_ORDER[i % 6]
            self.liu_shen[i] = l.liushen

    # -------------------- 空亡 --------------------
    def assign_empty(self):
        """计算空亡"""
        empty_branches = EMPTY_BRANCH.get(self.day_branch, [])
        self.empty = [l.pos for l in self.lines if l.branch in empty_branches]
        for l in self.lines:
            if l.pos in self.empty:
                l.state = "空亡"

    # -------------------- 冲合 --------------------
    def analyze_conflicts(self):
        """分析冲合"""
        def check_conflict_combine(branch1, branch2, i, j, table):
            pair = (branch1, branch2)
            if pair in table:
                return {"lines": (str(i + 1), str(j + 1)), "type": table[pair]}
            return None

        conflicts = []
        # 卦爻之间
        for i, l1 in enumerate(self.lines):
            for j, l2 in enumerate(self.lines):
                if i >= j: continue
                for table in [CLASH, COMBINE]:
                    res = check_conflict_combine(l1.branch, l2.branch, i, j, table)
                    if res: conflicts.append(res)

        # 日支/月支与爻
        for i, l in enumerate(self.lines):
            for branch in [self.day_branch, self.month_branch]:
                for table in [CLASH, COMBINE]:
                    res = check_conflict_combine(branch, l.branch, i, l.pos, table)
                    if res: conflicts.append(res)

        self.conflicts = conflicts

    # -------------------- 卦名 --------------------
    def generate_hexagram_name(self, hexagram):
        return "".join(["阳" if n in [7, 9] else "阴" for n in hexagram])

    def assign_hexagram_names(self):
        lower = self.generate_hexagram_name(self.original[:3])
        upper = self.generate_hexagram_name(self.original[3:])
        self.base_name = f"上{upper}下{lower}"

        lower_t = self.generate_hexagram_name(self.transformed[:3])
        upper_t = self.generate_hexagram_name(self.transformed[3:])
        self.trans_name = f"上{upper_t}下{lower_t}"

    # -------------------- 初始化 --------------------
    def initialize(self):
        """生成完整卦象及爻信息"""
        self.cast()
        self.calc_time()
        self.build_lines()
        self.enrich_lines()
        self.mark_shi_ying()
        self.assign_liu_shen()
        self.assign_empty()
        self.analyze_conflicts()
        self.assign_hexagram_names()

    # -------------------- 前端/UI --------------------
    def ui_data(self):
        return {
            "question": self.question,
            "coins": self.original,
            "moving": self.moving,
            "day_branch": self.day_branch,
            "month_branch": self.month_branch,
            "empty": self.empty,
            "conflicts": self.conflicts,
            "base_name": self.base_name,
            "trans_name": self.trans_name,
            "hexagram_name": self.hexagram_name,
            "main_gua": self.main_gua,  # ✅ 保证 analyze_yongshen 可用
            "palace": self.palace,
            "shi_pos": self.shi_pos,
            "ying_pos": self.ying_pos,
            "lines": [l.__dict__ for l in self.lines],
            "liu_shen_order": self.liu_shen
        }

    def summary(self):
        return self.ui_data()