from classes import Node
import NFA

class Leaf(Node.Node):

    def __init__(self, val=''):
        super().__init__()
        self.val = val

    def set_val(self, val):
        self.left = val
        return self

    def makeNFA(self, start=True, end=False, nameDigit=[0]):
        self.startnode = NFA.NFA(start, end, nameDigit[0])
        nameDigit[0] = nameDigit[0] + 1
        self.endnode = NFA.NFA(end, start, nameDigit[0])
        self.startnode.transitions.append(self.val)
        self.startnode.NFAchildren.append(self.endnode)
        nameDigit[0] = nameDigit[0] + 1
        return self.startnode

