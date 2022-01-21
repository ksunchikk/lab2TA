class DFA:

    def __init__(self, nodes=[], nameDigit=0):
        self.nodeName = 'D-node ' + str(nameDigit)
        self.nodes = nodes
        self.transitions = []
        self.DFAchildren = []
        self.startnode = False
        self.endnode = False
        self.error = False
        self.nameDigit = nameDigit
    def nextNode(self, c):
        if self.transitions.count(c) == 0:
            return None
        i = 0
        for cur in self.transitions:
            if cur == c:
                return self.DFAchildren[i]
            i += 1
        return None




