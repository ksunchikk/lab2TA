import SyntaxTree
import kpath
import createDFA
import RegExp
#string = '(a|bd...c)...bd...'
# (((a|$)|((a|$))...(a|$))|(b|((a|$))...b)(((d|$)|c((a|$))...b))...(c|c((a|$))...(a|$)))
string = '(a|bd...c)...|(a|bd...c)...bd...'
# (((a|$)|((a|$))...(a|$))|(b'
#print("Syntax 1")
a = SyntaxTree.SyntaxTree(string)
a.makeSyntaxTree()
#a.printTree(a.nodeList[0], 4)
#print("\n\nNFA 1")
a.createNFA()
a.printNFA(a.nodeList[0], 4)
b = createDFA.createDFA(a.nodeList[0].child, a.expAlphabet, 0)
c = createDFA.minimizeDFA(b, a.expAlphabet)
#print("\n\nDFA 1")
#createDFA.printDfa(b)
#print("\n\nmDFA 1\n\n")
createDFA.printDfa(c)
#print("\n\n")
sty = kpath.kPathRecovery(c)
print(sty)
cur = RegExp.RegExp(sty)
#createDFA.printDfa(cur.DFAutomata)
createDFA.printDfa(cur.automata)
#print(cur.findall("bddd"))
#createDFA.printDfa(createDFA.DFADifference(c, cc, a.expAlphabet, aa.expAlphabet))
#createDFA.printDfa(createDFA.DFAComplement(c, a.expAlphabet))

