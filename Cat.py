from classes import Binary
from classes import Group
import NFA

class Cat(Binary.Binary):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

    def makeNFA(self, start=True, end=False, nameDigit=[0]):
        self.startnode = NFA.NFA(start, end, nameDigit[0])
        nameDigit[0] = nameDigit[0] + 1
        self.endnode = NFA.NFA(end, start, nameDigit[0])
        nameDigit[0] = nameDigit[0] + 1
        if type(self.left) != Group.Group and type(self.right) != Group.Group:
            self.startnode.transitions.append('#')
            self.startnode.NFAchildren.append(self.left.makeNFA(False, False, nameDigit))
            self.left.endnode.NFAchildren.append(self.right.makeNFA(False, False, nameDigit))
            self.left.endnode.transitions.append('#')
            self.right.endnode.NFAchildren.append(self.endnode)
            self.right.endnode.transitions.append('#')
            return self.startnode
        elif type(self.left) != Group.Group and type(self.right) == Group.Group:
            self.startnode.transitions.append('#')
            self.startnode.NFAchildren.append(self.left.makeNFA(False, False, nameDigit))
            self.left.endnode.NFAchildren.append(self.right.makeNFA(False, False, nameDigit))
            self.left.endnode.transitions.append('#')
            self.right.child.endnode.NFAchildren.append(self.endnode)
            self.right.child.endnode.transitions.append('#')
            return self.startnode
        elif type(self.left) == Group.Group and type(self.right) == Group.Group:
            self.startnode.transitions.append('#')
            self.startnode.NFAchildren.append(self.left.makeNFA(False, False, nameDigit))
            self.left.child.endnode.NFAchildren.append(self.right.makeNFA(False, False, nameDigit))
            self.left.child.endnode.transitions.append('#')
            self.right.child.endnode.NFAchildren.append(self.endnode)
            self.right.child.endnode.transitions.append('#')
            return self.startnode
        else:
            self.startnode.transitions.append('#')
            self.startnode.NFAchildren.append(self.left.makeNFA(False, False, nameDigit))
            self.left.child.endnode.NFAchildren.append(self.right.makeNFA(False, False, nameDigit))
            self.left.child.endnode.transitions.append('#')
            self.right.endnode.NFAchildren.append(self.endnode)
            self.right.endnode.transitions.append('#')
            return self.startnode


