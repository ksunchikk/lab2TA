from classes import Node
import NFA
from classes import Leaf

class SquareBrackets(Node.Node):

    def __init__(self, child=[]):
        super().__init__()
        self.child = child

    def makeNFA(self, start=True, end=False, nameDigit=[]):
        self.startnode = NFA.NFA(start, end, nameDigit[0])
        nameDigit[0] = nameDigit[0] + 1
        self.startnode.transitions.append('#')
        i = 0
        cur = []
        self.endnode = NFA.NFA(end, start, nameDigit[0])
        nameDigit[0] = nameDigit[0] + 1
        while i < len(self.child):
            cur.append(Leaf.Leaf(self.child[i].val))
            cur[i].makeNFA(end, end, nameDigit)
            cur[i].endnode.NFAchildren.append(self.endnode)
            cur[i].endnode.transitions.append('#')
            self.startnode.NFAchildren.append(cur[i].startnode)
            i += 1
        nameDigit[0] = nameDigit[0] + 1
        return self.startnode
        