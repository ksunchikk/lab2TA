import copy

from classes import Unary
import NFA
from classes import Leaf
from classes import Group

class Repeat(Unary.Unary):
    def __init__(self, child=None, am=0):
        super().__init__(child)
        self.children = []
        self.amount = am

    def makeNFA(self, start=True, end=False, nameDigit=[]):
        self.startnode = NFA.NFA(start, end, nameDigit[0])
        nameDigit[0] = nameDigit[0] + 1
        self.endnode = NFA.NFA(end, start, nameDigit[0])
        self.startnode.transitions.append('#')
        i = 0
        while i < self.amount:
            if type(self.child) != Group.Group:
                self.children.append(copy.copy(self.child))
            else:
                self.children.append(copy.copy(self.child.child))
            i += 1
        i = 0
        cur=[]
        nameDigit[0] = nameDigit[0] + 1
        while i < self.amount:
            if type(self.children[i]) != Group.Group:
                cur.append(self.children[i])
            else:
                cur.append(self.children[i].child)
            cur[i].makeNFA(False, False, nameDigit)
            if i > 0:
                cur[i - 1].endnode.NFAchildren.append(cur[i].startnode)
                cur[i - 1].endnode.transitions.append('#')
            i += 1
        nameDigit[0] = nameDigit[0] + 1
        cur[self.amount - 1].endnode.NFAchildren.append(self.endnode)
        cur[self.amount - 1].endnode.transitions.append('#')
        self.startnode.NFAchildren.append(cur[0].startnode)
        return self.startnode
