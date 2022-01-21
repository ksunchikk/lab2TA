import collections
import functools

import DFA
import RegExp


def inDnodes(nodes, dnodes):
    flag = False
    j = 0
    for i in dnodes:
        if collections.Counter(i.nodes) == collections.Counter(nodes):
            flag = True
        else:
            flag = False
        if flag:
            return [True, j]
        flag = False
        j+=1
    return [False]

def printDfa(nodes):
    for n in nodes:
        print("name:{nodeName}  start:{startnode}  end:{endnode}".format(nodeName=n.nodeName, endnode=n.endnode, startnode=n.startnode))
        print(n.nodes)
        i = 0
        while i < len(n.DFAchildren):
            print("transition: {transition}   child:{child}".format(transition=n.transitions[i],child=n.DFAchildren[i].nodeName))
            i += 1

def eTran(node):
    dnodes = []
    dnodes.append(node)
    i = 0
    while i < len(dnodes):
        k = 0
        while k < len(dnodes[i].NFAchildren):
            tmp = dnodes[i].transitions[0]
            if  tmp == '#' or len(tmp) == 0:
                if dnodes.count(dnodes[i].NFAchildren[k])==0:
                    dnodes.append(dnodes[i].NFAchildren[k])
            k += 1
        i += 1
    return dnodes

def createDFA(start, alphabet, nameDigit):
    curstart = start.startnode
    while curstart.start != True:
        start = start.child
        curstart = start.startnode
    dnodes = []
    digit = []
    digit.append(nameDigit)
    startnode = DFA.DFA(nodes = eTran(curstart), nameDigit=digit[nameDigit])
    nameDigit += 1
    digit.append(nameDigit)
    startnode.startnode = True
    for i in startnode.nodes:
        if i.end == True:
            startnode.endnode = True
    dnodes.append(startnode)
    k = 0
    nodes = []
    while k < len(dnodes):
        for c in alphabet:
            for node in dnodes[k].nodes:
                j = 0
                for tr in node.transitions:
                    if tr == c:
                        nodes.append(node.NFAchildren[j])
                    j+=1
            cur = []
            for tr in nodes:
                tmp = eTran(tr)
                for tmp1 in tmp:
                    if cur.count(tmp1) == 0:
                        cur.append(tmp1)
            nodes = []
            if inDnodes(cur, dnodes)[0]:
                dnodes[k].transitions.append(c)
                dnodes[k].DFAchildren.append(dnodes[inDnodes(cur, dnodes)[1]])
                continue
            tr = DFA.DFA(cur, digit[nameDigit])
            nameDigit += 1
            digit.append(nameDigit)
            if len(tr.nodes) == 0:
                tr.error = True
            for j in tr.nodes:
                if j.end == True:
                    tr.endnode = True
            dnodes[k].transitions.append(c)
            dnodes[k].DFAchildren.append(tr)
            dnodes.append(tr)
        k+=1
    return dnodes

def similarGroup(allGroups, dnode):
    i = 0
    while i < len(allGroups):
        for tmp in allGroups[i]:
            if tmp == dnode:
                return i
        i += 1
    return -1

def minimizeDFA(dnodes, alphabet):
    fGroup = []
    sGroup = []
    for dnode in dnodes:
        if dnode.endnode:
            fGroup.append(dnode)
        else:
            sGroup.append(dnode)
    allGroups = []
    allGroups.append(fGroup)
    if len(sGroup) != 0:
        allGroups.append(sGroup)
    endAlgorithm = True
    while endAlgorithm:
        i = 0
        endAlgorithm = False
        while i < len(allGroups):
            for c in alphabet:
                group = dict()
                miniGroup = []
                for dnode in allGroups[i]:
                    k = 0
                    for tr in dnode.transitions:
                       if tr == c:
                           miniGroup.append([dnode, dnode.DFAchildren[k]])
                       k += 1
                group[c] = miniGroup
                serNumber = similarGroup(allGroups, group[c][0][1])
                fGroup = []
                sGroup = []
                contGroup = False
                for tr in group[c]:
                    if similarGroup(allGroups, tr[1]) != serNumber:
                        fGroup.append(tr[0])
                        endAlgorithm = True
                        contGroup = True
                    else:
                        sGroup.append(tr[0])
                if not(contGroup):
                    continue
                allGroups[i:i+1] = [sGroup, fGroup]
                i -=1
                break
            i +=1
    minimalDFA = []
    createMinimalDFA(minimalDFA, allGroups)
    return minimalDFA

def createMinimalDFA(minimalDFA, allGroups):
    nameDigit = 0
    while nameDigit < len(allGroups):
        minimalDFA.append(DFA.DFA(allGroups[nameDigit], nameDigit))
        nameDigit += 1
    i = 0
    while i < len(allGroups):
        for dnode in allGroups[i]:
            k = 0
            while k < len(dnode.transitions):
                if minimalDFA[i].transitions.count(dnode.transitions[k]) != 0:
                    k += 1
                    continue
                minimalDFA[i].transitions.append(dnode.transitions[k])
                minimalDFA[i].DFAchildren.append(minimalDFA[similarGroup(allGroups, dnode.DFAchildren[k])])
                k += 1
            if dnode.endnode == True:
                minimalDFA[i].endnode = True
            if dnode.startnode == True:
                minimalDFA[i].startnode = True
            if dnode.error == True:
                minimalDFA[i].error = True
        i += 1

def DFADifference(fDFA, sDFA, alphabet1, alphabet2):
    DifferenceStates = []
    DifferenceAlphabet = set()
    for c in alphabet1:
        DifferenceAlphabet.add(c)
    for c in alphabet2:
        DifferenceAlphabet.add(c)
    iIndex = 0
    errorStates = []
    for i in fDFA:
        jIndex = 0
        for j in sDFA:
            index = iIndex * len(sDFA) + jIndex
            DifferenceStates.append(DFA.DFA(nameDigit=index))
            if i.endnode == True and j.endnode == False:
                DifferenceStates[index].endnode = True
            else:
                DifferenceStates[index].endnode = False
            if i.startnode and j.startnode:
                DifferenceStates[index].startnode = True
            else:
                DifferenceStates[index].startnode = False

            if i.error and j.error:
                DifferenceStates[index].error = True
                errorStates.append(DifferenceStates[index])
            jIndex += 1
        iIndex += 1
    iIndex = 0
    for i in fDFA:
        jIndex = 0
        for j in sDFA:
            index = iIndex * len(sDFA) + jIndex
            iTRindex = 0
            for iTR in i.transitions:
                jTRindex = 0
                for jTR in j.transitions:
                    if (iTR == jTR):
                        tmp = inTrans(fDFA[iIndex].DFAchildren[iTRindex], fDFA) * len(sDFA) + inTrans(sDFA[jIndex].DFAchildren[jTRindex],sDFA)
                        DifferenceStates[index].DFAchildren.append(DifferenceStates[tmp])
                        DifferenceStates[index].transitions.append(jTR)
                    jTRindex += 1
                iTRindex += 1
            jIndex += 1
        iIndex += 1

    if sorted(alphabet1) != sorted(alphabet2):
        err = 0
        if len(errorStates) == 0:
            err = DFA.DFA(10)
            for tr in set.intersection(alphabet1, alphabet2):
                err.DFAchildren.append(err)
                err.transitions.append(tr)
            DifferenceStates.append(err)
        alphabet = set.union(alphabet1, alphabet2)
        if len(errorStates) != 0:
            err = errorStates[0]
        for c in alphabet:
            if (inTrans(c,alphabet1) == -1) or (inTrans(c,alphabet2) == -1):
                    for dnode in DifferenceStates:
                        if (inTrans(c, dnode.transitions) == -1):
                            dnode.transitions.append(c)
                            dnode.DFAchildren.append(err)
    return DifferenceStates
def DFAComplement(automata, fDFA, alphabet):
    string = ''
    i = 0
    for c in alphabet:
        if i != len(alphabet) - 1:
            string = string + c + '|'
        else:
            string = string + c
        i +=1
    string = '(' + string +')...'
    universe = RegExp.RegExp(string)
    return DFADifference(universe.automata, fDFA, alphabet, alphabet)

def inTrans(dnode, fDFA):
    i = 0
    for node in fDFA:
        if node == dnode:
            return i
        i+=1
    return -1