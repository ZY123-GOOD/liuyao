from datetime import datetime
from engine.coin import build_hexagram
from engine.hexagram_builder import build
from knowledge.calendar import get_day_branch, get_month_branch
from knowledge.branches import get_element
from knowledge.liuqin import get_relative

LIU_SHEN_ORDER = ["青龙","朱雀","勾陈","腾蛇","白虎","玄武"]

# 空亡对照表（简化版）
EMPTY_BRANCH = {
    "甲子":["戌","亥"], "乙丑":["戌","亥"], "丙寅":["子","丑"],
    "丁卯":["子","丑"], "戊辰":["寅","卯"], "己巳":["寅","卯"],
    "庚午":["辰","巳"], "辛未":["辰","巳"], "壬申":["午","未"],
    "癸酉":["午","未"], "甲戌":["申","酉"], "乙亥":["申","酉"]
}

# 冲合表（可拓展）
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

    def cast(self):
        self.original = self.coins if self.coins else build_hexagram()
        self.moving = [i+1 for i,v in enumerate(self.original) if v in [6,9]]
        self.transformed = self.transform()

    def transform(self):
        new=[]
        for i,l in enumerate(self.original):
            val = 7 if l==6 else 8 if l==9 else l
            new.append(val)
            if self.lines:
                self.lines[i].number = l
        return new

    def calc_time(self):
        self.day_branch = get_day_branch(self.datetime)
        self.month_branch = get_month_branch(self.datetime)
        self.day_element = get_element(self.day_branch)
        self.month_element = get_element(self.month_branch)

    def build_lines(self):
        self.lines = build(self.original, self.day_element)
        for i,l in enumerate(self.lines):
            l.number = self.original[i]

    def enrich_lines(self):
        for l in self.lines:
            l.set_element(get_element(l.branch))
            l.set_relative(get_relative(self.day_element, l.element))
            l.moving = (l.pos in self.moving)

    def mark_shi_ying(self):
        self.lines[5].shi = True
        self.lines[2].ying = True

    def assign_liu_shen(self):
        for i,l in enumerate(self.lines):
            l.liushen = LIU_SHEN_ORDER[i%6]
            self.liu_shen[i] = l.liushen

    # ------------------ 空亡改进 ------------------
    def assign_empty(self):
        """
        根据日支计算哪些爻落空亡
        返回爻位列表，例如 [2,5]
        """
        empty_branches = EMPTY_BRANCH.get(self.day_branch, [])
        self.empty = [l.pos for l in self.lines if l.branch in empty_branches]

    # 冲合改进
    def analyze_conflicts(self):
        conflicts = []
        # 卦爻之间
        for i,l1 in enumerate(self.lines):
            for j,l2 in enumerate(self.lines):
                if i>=j: continue
                pair = (l1.branch, l2.branch)
                if pair in CLASH:
                    conflicts.append({"lines":(i+1,j+1),"type":"冲"})
                elif pair in COMBINE:  # 用全局字典 COMBINE
                    conflicts.append({"lines":(i+1,j+1),"type":"合"})
        # 日支/月支与卦爻冲合
        for i,l in enumerate(self.lines):
            pair_day = (self.day_branch, l.branch)
            pair_month = (self.month_branch, l.branch)
            if pair_day in CLASH:
                conflicts.append({"lines":("日",l.pos),"type":"冲"})
            elif pair_day in COMBINE:
                conflicts.append({"lines":("日",l.pos),"type":"合"})
            if pair_month in CLASH:
                conflicts.append({"lines":("月",l.pos),"type":"冲"})
            elif pair_month in COMBINE:
                conflicts.append({"lines":("月",l.pos),"type":"合"})
        self.conflicts = conflicts

    def assign_hexagram_names(self):
        lower = "".join(["阳" if n in [7,9] else "阴" for n in self.original[:3]])
        upper = "".join(["阳" if n in [7,9] else "阴" for n in self.original[3:]])
        self.base_name = f"上{upper}下{lower}"
        lower_t = "".join(["阳" if n in [7,9] else "阴" for n in self.transformed[:3]])
        upper_t = "".join(["阳" if n in [7,9] else "阴" for n in self.transformed[3:]])
        self.trans_name = f"上{upper_t}下{lower_t}"

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
                    "number":l.number
                } for l in self.lines
            ],
            "liu_shen_order": self.liu_shen
        }

    def summary(self):
        return self.ui_data()