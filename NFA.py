class NFA:
    def __init__(self, start = False, end = False, nameDigit=0):
        self.nodeName ='node '+str(nameDigit)
        self.start = start
        self.end = end
        self.transitions = []
        self.NFAchildren = []
        self.processed = False

