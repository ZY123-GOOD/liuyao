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
        self.original = self.transformed = self.lines = self.moving = None

        # 时间与五行
        self.day_branch = self.month_branch = self.day_element = self.month_element = None

        # 六神/空亡/冲合
        self.liu_shen = [None] * 6
        self.empty = []
        self.conflicts = []

        # 卦名/世应/卦宫
        self.base_name = self.trans_name = self.hexagram_name = None
        self.palace = None
        self.shi_pos = None
        self.ying_pos = None
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
        """计算并设置日支、月支、日五行、月五行"""
        self.day_branch = get_day_branch(self.datetime)
        self.month_branch = get_month_branch(self.datetime)
        self.day_element = get_element(self.day_branch)
        self.month_element = get_element(self.month_branch)

    # -------------------- 爻生成/六亲/状态 --------------------
    def build_lines(self):
        """根据原始卦象和五行构建爻"""
        result = build(self.original, self.day_element)
        self.lines = result["original_lines"]

        # 卦宫/世应/卦名
        self.palace = result.get("palace", "未知")
        self.shi_pos = result.get("shi_pos", 3)  # 默认第三爻为世爻
        self.ying_pos = result.get("ying_pos", 6)  # 默认第六爻为应爻
        self.hexagram_name = result.get("hexagram_name", "未知卦")

        for i, l in enumerate(self.lines):
            l.number = self.original[i]
            l.state = "平"

        self.shi_yao = self.lines[self.shi_pos - 1]  # 世爻

    def enrich_lines(self):
        """为每个爻填充五行和六亲等信息"""
        for l in self.lines:
            l.set_element(get_element(l.branch))
            # 用日主五行计算六亲
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
        """计算并标记空亡爻"""
        empty_branches = EMPTY_BRANCH.get(self.day_branch, [])
        self.empty = [l.pos for l in self.lines if l.branch in empty_branches]
        for l in self.lines:
            if l.pos in self.empty:
                l.state = "空亡"

    # -------------------- 冲合 --------------------
    def analyze_conflicts(self):
        """分析冲合，检查卦爻之间以及日月支与卦爻的冲合"""
        def check_conflict_combine(branch1, branch2, i, j, conflict_type):
            pair = (branch1, branch2)
            if pair in conflict_type:
                return {"lines": (str(i + 1), str(j + 1)), "type": conflict_type[pair]}
            return None

        conflicts = []

        # 卦爻之间的冲合
        for i, l1 in enumerate(self.lines):
            for j, l2 in enumerate(self.lines):
                if i >= j: continue
                res = check_conflict_combine(l1.branch, l2.branch, i, j, CLASH)
                if res:
                    conflicts.append(res)
                res = check_conflict_combine(l1.branch, l2.branch, i, j, COMBINE)
                if res:
                    conflicts.append(res)

        # 日支/月支与卦爻的冲合
        for i, l in enumerate(self.lines):
            for branch in [self.day_branch, self.month_branch]:
                res = check_conflict_combine(branch, l.branch, i, l.pos, CLASH)
                if res:
                    conflicts.append(res)
                res = check_conflict_combine(branch, l.branch, i, l.pos, COMBINE)
                if res:
                    conflicts.append(res)

        self.conflicts = conflicts

    # -------------------- 卦名 --------------------
    def generate_hexagram_name(self, hexagram):
        """根据卦象生成卦名"""
        return "".join(["阳" if n in [7, 9] else "阴" for n in hexagram])

    def assign_hexagram_names(self):
        """生成卦名"""
        lower = self.generate_hexagram_name(self.original[:3])
        upper = self.generate_hexagram_name(self.original[3:])
        self.base_name = f"上{upper}下{lower}"

        lower_t = self.generate_hexagram_name(self.transformed[:3])
        upper_t = self.generate_hexagram_name(self.transformed[3:])
        self.trans_name = f"上{upper_t}下{lower_t}"

    # -------------------- 初始化 --------------------
    def initialize(self):
        """初始化六爻占卜的各项数据"""
        self.cast()
        self.calc_time()
        self.build_lines()
        self.enrich_lines()
        self.mark_shi_ying()
        self.assign_liu_shen()
        self.assign_empty()
        self.analyze_conflicts()
        self.assign_hexagram_names()

    # -------------------- UI 数据 --------------------
    def ui_data(self):
        """返回用于前端显示的数据"""
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
            "palace": self.palace,
            "shi_pos": self.shi_pos,
            "ying_pos": self.ying_pos,
            "lines": [{
                "pos": l.pos,
                "branch": l.branch,
                "element": l.element,
                "relative": l.relative,
                "moving": l.moving,
                "shi": l.shi,
                "ying": l.ying,
                "liushen": l.liushen,
                "state": l.state,
                "number": l.number
            } for l in self.lines],
            "liu_shen_order": self.liu_shen
        }

    def summary(self):
        """返回占卜的整体结果数据"""
        return self.ui_data()