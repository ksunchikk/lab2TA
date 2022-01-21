from classes import Unary


class Group(Unary.Unary):
    def __init__(self, child=None, num=1):
        super().__init__(child)
        self.num = num

    def makeNFA(self, start=True, end=False, nameDigit=[0]):
        self.child.makeNFA(start,end,nameDigit)
        return self.child.startnode