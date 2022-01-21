from classes import Unary
from classes import Group
import NFA

class Clini(Unary.Unary):
    def __init__(self, child=None):
        super().__init__(child)

    def makeNFA(self, start=True, end=False, nameDigit=[0]):
        self.startnode = NFA.NFA(start, end, nameDigit[0])
        nameDigit[0] = nameDigit[0] + 1
        self.endnode = NFA.NFA(end, start, nameDigit[0])
        self.startnode.transitions.append('#')
        nameDigit[0] = nameDigit[0] + 1
        newchild = self.child
        if type(newchild) != Group.Group:
            self.startnode.NFAchildren.append(self.child.makeNFA(False, False, nameDigit))
            nameDigit[0] = nameDigit[0] + 1
            self.startnode.NFAchildren.append(self.endnode)
            self.child.endnode.NFAchildren.append(self.child.startnode)
            self.child.endnode.NFAchildren.append(self.endnode)
            self.child.endnode.transitions.append('#')
            return self.startnode
        else:
            while type(newchild) == Group.Group:
                newchild = newchild.child
            self.startnode.NFAchildren.append(newchild.makeNFA(False, False, nameDigit))
            nameDigit[0] = nameDigit[0] + 1
            self.startnode.NFAchildren.append(self.endnode)
            newchild.endnode.NFAchildren.append(newchild.startnode)
            newchild.endnode.NFAchildren.append(self.endnode)
            newchild.endnode.transitions.append('#')
            return self.startnode

