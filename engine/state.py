class Line:

    def __init__(

        self,
        pos,
        branch,
        day_element,
        moving=False,
        shi=False,
        ying=False

    ):

        self.pos=pos

        self.branch=branch

        self.element=None

        self.relative=None

        self.moving=moving

        self.shi=shi

        self.ying=ying

        self.day_element=day_element


    def set_element(self,element):

        self.element=element


    def set_relative(self,relative):

        self.relative=relative