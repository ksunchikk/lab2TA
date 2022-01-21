import NFA
class Node(object):

    def __init__(self):

        self.startnode = NFA.NFA()
        self.endnode = NFA.NFA()



    def is_processed(self):
        return self.processed

    def set_processed(self, pr):
        self.processed = pr
        return self

    def makeNFA(self,start,end, nameDigit=[]):
        return self.startnode








