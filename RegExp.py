import NFA
import DFA
import SyntaxTree
import createDFA
import kpath

class RegExp():
    def __init__(self, exp=''):
        self.string = exp
        self.DFAutomata = None
        self.syntaxTree = None
        self.automata = self.compile()
        self.alphabet = self.syntaxTree.expAlphabet
    def compile(self):
        self.syntaxTree = SyntaxTree.SyntaxTree(self.string)
        self.syntaxTree.makeSyntaxTree()
        self.syntaxTree.createNFA()
        self.DFAutomata = createDFA.createDFA(self.syntaxTree.nodeList[0].child, self.syntaxTree.expAlphabet, 0)
        tmp = createDFA.minimizeDFA(self.DFAutomata, self.syntaxTree.expAlphabet)
        self.automata = tmp
        return tmp
    def difference(self, dnodes, alpabet):
        return createDFA.DFADifference(self.automata, dnodes, self.alphabet, alpabet)
    def comlement(self):
        return createDFA.DFAComplement(self, self.automata, self.alphabet)
    def recovery(self):
        return kpath.kPathRecovery(self.automata)
    def findall(self, string):
        newstring = string
        result = []
        i = 0
        while i < len(newstring):
            j = i
            while j < len(newstring):
                k = i
                curstring = ''
                while k <= j:
                    curstring += newstring[k]
                    k+=1
                flag = self.check(curstring)
                if flag:
                    result.append(curstring)
                    newstring = newstring[:i] + newstring[j + 1:]
                    j = i
                else:
                    j+=1
            i += 1
        return result
    def check(self, string):
        startnode = None
        for dnode in self.automata:
            if dnode.startnode:
                startnode = dnode
                break
        for c in string:
            if not(self.alphabet.__contains__(c)):
                return False
            startnode = startnode.nextNode(c)
        return startnode.endnode