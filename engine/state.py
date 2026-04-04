class Line:
    def __init__(self,
        pos,
        branch,
        day_element,
        yin_yang,
        number,
        moving=False
    ):

        self.pos=pos

        self.branch=branch

        self.day_element=day_element

        self.yin_yang=yin_yang

        self.number=number

        self.moving=moving
        self.element = None
        self.state=None

        self.relative=None
        self.shi = False  # 标记是否为世爻
        self.ying = False  # 标记是否为应爻
        self.liushen=None

    def set_element(self, element):
        self.element = element

    def set_relative(self, relative):
        self.relative = relative