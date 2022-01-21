def createBasis(kMatrix, allSymbols, dnodes):
    dIndex = 0
    for dnode in dnodes:
        trIndex = 0
        for tr in dnode.DFAchildren:
            symbol = dnode.transitions[trIndex]
            if inTrans(symbol, allSymbols) != -1:
                symbol = '\\'+symbol
            if kMatrix[dIndex][tr.nameDigit][0] == '':
                kMatrix[dIndex][tr.nameDigit][0] = symbol
            else:
                kMatrix[dIndex][tr.nameDigit][0] = kMatrix[dIndex][tr.nameDigit][0] + '|' + symbol
            trIndex += 1
        if kMatrix[dIndex][dIndex][0] == '':
            kMatrix[dIndex][dIndex][0] = '$'
        else:
            kMatrix[dIndex][dIndex][0] = newOR(kMatrix[dIndex][dIndex][0], '$')
        dIndex += 1
    return kMatrix
def kPathRecovery(dnodes):
    kMatrix = list()
    i = 0
    while i < len(dnodes):
        kMatrix.append([])
        j = 0
        while j < len(dnodes):
            kMatrix[i].append([])
            k = 0
            while k < len(dnodes) + 1:
                kMatrix[i][j].append('')
                k += 1
            j += 1
        i += 1
    allSymbols = ['$', '...', '{', '}', '(', ')', '|', '[', ']', '\\', ':']
    createBasis(kMatrix, allSymbols, dnodes)
    startNode = None
    resPath = ''
    for dnode in dnodes:
        if dnode.startnode == True:
            startNode = dnode
    for dnode in dnodes:
        if dnode.endnode:
            curPath = kpath(kMatrix, len(dnodes), startNode, dnode, dnodes)
            if len(resPath) != 0 and len(curPath) != 0:
                resPath = resPath + '|'
            resPath = resPath + curPath
    return resPath
def kpath(kMatrix, k, fDnode, sDnode, dnodes):
    resPath = ''
    resIK = ''
    resKJ = ''
    res = ''
    fIndex = fDnode.nameDigit
    sIndex = sDnode.nameDigit
    if k == 0:
        return kMatrix[fIndex][sIndex][0]
    if len(kMatrix[fIndex][sIndex][k]) != 0:
        return kMatrix[fIndex][sIndex][k]
    if len(kMatrix[fIndex][sIndex][k-1]) == 0:
        resPath = kpath(kMatrix, k - 1, fDnode, sDnode, dnodes)
    else:
        resPath = kMatrix[fIndex][sIndex][k-1]
    if len(kMatrix[fIndex][k - 1][k-1]) == 0:
        resIK = kpath(kMatrix, k - 1, fDnode, dnodes[k - 1],  dnodes)
    else:
        resIK = kMatrix[fIndex][k - 1][k-1]
    if len(kMatrix[k - 1][sIndex][k - 1]) == 0:
        resKJ = kpath(kMatrix, k - 1, dnodes[k - 1], sDnode,  dnodes)
    else:
        resKJ = kMatrix[k - 1][sIndex][k - 1]
    if len(resIK) != 0 and len(resKJ) != 0:
        if len(kMatrix[k - 1][k - 1][k - 1]) == 0:
            resKK = kpath(kMatrix, k - 1, dnodes[k - 1], dnodes[k - 1], dnodes)
        else:
            resKK = kMatrix[k - 1][k - 1][k - 1]
        if len(resKK) != 0 and resKK != '$':
            if resIK == resKK:
                resIK = '(' + resIK + ')...'
            else:
                resIK = resIK + '(' + resKK + ')...'
        res = resIK + resKJ
        resPath = newOR(resPath, res)
    kMatrix[fIndex][sIndex][k] = resPath
    #print(resPath + " " + str(k) + " " + str(fIndex) + " " + str(sIndex))
    return resPath
def isBR(res, k):
    i = 1
    if res[k] == ')' and k == 0 or res[k - 1] != '\\':
            while True:
                k -= 1
                if k < 0 and i > 0:
                    break
                if res[k] == ')' and k == 0 or res[k - 1] != '\\':
                    i += 1
                if res[k] == '(' and k == 0 or res[k - 1] != '\\':
                    i -= 1
                if i == 0:
                    break
            if k < 0 and i > 0:
                return -1
            return k
    return -1
def newOR(string, symbol):
    res = string
    if len(res) != 0:
        if(isBR(res, len(res) - 1) == 0):
            res = res[:len(res)-1] + res[len(res)-1:]
        else:
            res = '(' + res
        res += '|' + symbol + ')'
    else:
        res += symbol
    return res
def inTrans(dnode, fDFA):
    i = 0
    for node in fDFA:
        if node == dnode:
            return i
        i += 1
    return -1