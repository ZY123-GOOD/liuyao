from datetime import datetime
from engine.coin import build_hexagram
from engine.hexagram_builder import build
from knowledge.calendar import get_day_branch, get_month_branch
from knowledge.branches import get_element
from knowledge.liuqin import get_relative

LIU_SHEN_ORDER = ["青龙","朱雀","勾陈","腾蛇","白虎","玄武"]

EMPTY_BRANCH = {
    "甲子":["戌","亥"], "乙丑":["戌","亥"], "丙寅":["子","丑"],
    "丁卯":["子","丑"], "戊辰":["寅","卯"], "己巳":["寅","卯"],
    "庚午":["辰","巳"], "辛未":["辰","巳"], "壬申":["午","未"],
    "癸酉":["午","未"], "甲戌":["申","酉"], "乙亥":["申","酉"]
}

CLASH = {("子","午"):"冲", ("午","子"):"冲", ("寅","申"):"冲", ("申","寅"):"冲",
         ("巳","亥"):"冲", ("亥","巳"):"冲", ("卯","酉"):"冲", ("酉","卯"):"冲"}
COMBINE = {("子","丑"):"合", ("丑","子"):"合", ("寅","亥"):"合", ("亥","寅"):"合"}

class Divination:

    def __init__(self, question, gender=None, dt=None, coins=None):
        self.question = question
        self.gender = gender
        self.datetime = dt if dt else datetime.now()
        self.coins = coins

        self.original = None
        self.transformed = None
        self.lines = None
        self.moving = None

        self.day_branch = None
        self.month_branch = None
        self.day_element = None
        self.month_element = None

        self.liu_shen = [None]*6
        self.empty = []
        self.conflicts = []

        self.base_name = None
        self.trans_name = None

        self.shi_yao = None  # 世爻，用于六亲计算

    # -------------------- 卦生成 --------------------
    def cast(self):
        self.original = self.coins if self.coins else build_hexagram()
        self.moving = [i+1 for i,v in enumerate(self.original) if v in [6,9]]
        self.transformed = self.transform()

    def transform(self):
        new = []
        for i, l in enumerate(self.original):
            val = 7 if l == 6 else 8 if l == 9 else l
            new.append(val)
            if self.lines:
                self.lines[i].number = l
        return new

    # -------------------- 时间/五行 --------------------
    def calc_time(self):
        self.day_branch = get_day_branch(self.datetime)
        self.month_branch = get_month_branch(self.datetime)
        self.day_element = get_element(self.day_branch)
        self.month_element = get_element(self.month_branch)

    # -------------------- 爻生成/六亲/状态 --------------------
    def build_lines(self):
        self.lines = build(self.original, self.day_element)
        for i,l in enumerate(self.lines):
            l.number = self.original[i]
            l.state = "平"

        # 默认第三爻为世爻
        self.shi_yao = self.lines[2]

    def enrich_lines(self):
        for l in self.lines:
            l.set_element(get_element(l.branch))
            # 用世爻计算六亲
            l.set_relative(get_relative(self.shi_yao.element, l.element))
            l.moving = (l.pos in self.moving)
            # state 已初始化为平，可在后续空亡/冲合中更新

    def mark_shi_ying(self):
        self.lines[5].shi = True
        self.lines[2].ying = True

    def assign_liu_shen(self):
        for i,l in enumerate(self.lines):
            l.liushen = LIU_SHEN_ORDER[i%6]
            self.liu_shen[i] = l.liushen

    # -------------------- 空亡 --------------------
    def assign_empty(self):
        empty_branches = EMPTY_BRANCH.get(self.day_branch, [])
        self.empty = [l.pos for l in self.lines if l.branch in empty_branches]
        for l in self.lines:
            if l.pos in self.empty:
                l.state = "空亡"

    # -------------------- 冲合 --------------------
    def analyze_conflicts(self):
        conflicts = []
        seen = set()
        # 卦爻之间
        for i,l1 in enumerate(self.lines):
            for j,l2 in enumerate(self.lines):
                if i>=j: continue
                pair = (l1.branch, l2.branch)
                if pair in CLASH and pair not in seen:
                    conflicts.append({"lines":(i+1,j+1),"type":"冲"})
                    seen.add(pair)
                elif pair in COMBINE and pair not in seen:
                    conflicts.append({"lines":(i+1,j+1),"type":"合"})
                    seen.add(pair)
        # 日支/月支与卦爻冲合
        for i,l in enumerate(self.lines):
            for t, branch in [("日", self.day_branch), ("月", self.month_branch)]:
                pair = (branch, l.branch)
                if pair in CLASH and pair not in seen:
                    conflicts.append({"lines":(t,l.pos),"type":"冲"})
                    seen.add(pair)
                elif pair in COMBINE and pair not in seen:
                    conflicts.append({"lines":(t,l.pos),"type":"合"})
                    seen.add(pair)
        self.conflicts = conflicts

    # -------------------- 卦名 --------------------
    def assign_hexagram_names(self):
        lower = "".join(["阳" if n in [7,9] else "阴" for n in self.original[:3]])
        upper = "".join(["阳" if n in [7,9] else "阴" for n in self.original[3:]])
        self.base_name = f"上{upper}下{lower}"
        lower_t = "".join(["阳" if n in [7,9] else "阴" for n in self.transformed[:3]])
        upper_t = "".join(["阳" if n in [7,9] else "阴" for n in self.transformed[3:]])
        self.trans_name = f"上{upper_t}下{lower_t}"

    # -------------------- 初始化 --------------------
    def initialize(self):
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
            "lines":[
                {
                    "pos":l.pos,
                    "branch":l.branch,
                    "element":l.element,
                    "relative":l.relative,
                    "moving":l.moving,
                    "shi":l.shi,
                    "ying":l.ying,
                    "liushen":l.liushen,
                    "state":l.state,
                    "number":l.number
                } for l in self.lines
            ],
            "liu_shen_order": self.liu_shen
        }

    def summary(self):
        return self.ui_data()