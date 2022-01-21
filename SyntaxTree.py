from classes import Leaf
from classes import Or
from classes import Clini
from classes import Repeat
from classes import SquareBrackets
from classes import Brackets
from classes import Group
from classes import Cat
import NFA
class SyntaxTree:
	def __init__(self, string=''):
		self.string = '(' + string + ')'
		self.nodeList = []
		self.groupList = []
		self.bracketsList = []
		self.expAlphabet = set()
		self.autoNode = set()

	def makeNodeList(self):
		i=0
		openAm = 0
		closeAm = 0
		self.nodeList = []
		self.groupList = []
		self.bracketsList = []
		while i < len(self.string):
			c = self.string[i]
			if c == '\\':
				if i + 1 < len(self.string):
					i+=1
					self.expAlphabet.add(self.string[i])
					tmp = Leaf.Leaf(self.string[i])
					self.nodeList.append(tmp)
				else:
					raise Exception('Syntax error!')
			elif c == '$':
				tmp = Leaf.Leaf()
				self.nodeList.append(tmp)
			elif c == '|':
				if self.string[i + 1] != '|':
					tmp = Or.Or()
					self.nodeList.append(tmp)
				else:
					raise Exception('Syntax error!')
			elif c == '.':
				if self.string[i+1] == '.' and self.string[i+2] == '.' and self.string[i+3] != '.':
					tmp = Clini.Clini()
					self.nodeList.append(tmp)
					i+=2
				else:
					raise Exception('Syntax error!')
			elif c == '[':
				k = i
				if self.string[i + 1] == ']':
					raise Exception('Syntax error!')
				else:
					i += 1
					val = []
					while self.string[i] != ']':
						self.expAlphabet.add(self.string[i])
						val.append(Leaf.Leaf(self.string[i]))
						i += 1
						if i == len(self.string):
							raise Exception('Syntax error!')
				tmp = SquareBrackets.SquareBrackets(val)
				self.nodeList.append(tmp)
			elif c == '}':
				raise Exception('Syntax error!')
			elif c == ']':
				raise Exception('Syntax error!')
			elif c == '(':
				openAm+=1
				tmp = Brackets.OpenBracket()
				self.nodeList.append(tmp)
			elif c == ')':
				closeAm += 1
				tmp = Brackets.CloseBracket()
				self.nodeList.append(tmp)
			elif c == '{':
				k = i
				if self.string[i+1] == '}':
					raise Exception('Syntax error!')
				else:
					i += 1
					val = 0
					while self.string[i] != '}':
						if self.string[i].isnumeric():
							val *= 10
							val += int(self.string[i])
							i += 1
						else:
							raise Exception('Syntax error!')
						if (i-k) >= 3:
							raise Exception('Syntax error!')
						if val == 0:
							raise Exception('Syntax error!')
					tmp = Repeat.Repeat(am=val)
					self.nodeList.append(tmp)
			else:
				self.expAlphabet.add(self.string[i])
				tmp = Leaf.Leaf(self.string[i])
				self.nodeList.append(tmp)
			i+=1
		if openAm != closeAm:
			raise Exception('Syntax error!')

	def makeSyntaxTree(self):
		self.makeNodeList()
		groupCount = 0
		if len(self.nodeList) == 3 and type(self.nodeList[0]) == Brackets.OpenBracket and type(self.nodeList[1]) == Leaf.Leaf and type(self.nodeList[2]) == Brackets.CloseBracket:
			if self.nodeList[1].val == '':
				raise Exception('Empty string error!')
		i = 0
		while i < len(self.nodeList):
			node = self.nodeList[i]
			if type(node) == Brackets.OpenBracket:
				self.bracketsList.append((node, None))
			if type(node) == Brackets.CloseBracket:
				k = len(self.bracketsList) - 1
				while k >= 0:
					if self.bracketsList[k][1] == None:
						self.bracketsList[k] = (self.bracketsList[k][0], node)
						break
					k -= 1
			i += 1
		i = len(self.bracketsList) - 1
		while len(self.nodeList) != 1:
			flag = False
			i = len(self.bracketsList) - 1
			start = self.nodeList.index(self.bracketsList[i][0])
			end = self.nodeList.index(self.bracketsList[i][1])
			if type(self.nodeList[start + 1]) == Leaf.Leaf:
				if self.nodeList[start + 1].val == ':':
					self.nodeList.remove(self.nodeList[start + 1])
					end -= 1
				else:
					tmp = Group.Group(num=groupCount)
					self.groupList.append(tmp)
					groupCount += 1
					flag = True
			else:
				tmp = Group.Group(num=groupCount)
				self.groupList.append(tmp)
				groupCount += 1
				flag = True
			k = start+1
			while k < end:
				if type(self.nodeList[k]) == Repeat.Repeat:
					self.nodeList[k].child = self.nodeList[k - 1]
					self.nodeList.remove(self.nodeList[k - 1])
					end -= 1
				k+=1
			k = start+1
			while k < end:
				if type(self.nodeList[k]) == Clini.Clini:
					self.nodeList[k].child = self.nodeList[k-1]
					self.nodeList.remove(self.nodeList[k-1])
					end -=1
				k+=1
			k = start + 1
			while k < end:
				if type(self.nodeList[k]) != Or.Or and type(self.nodeList[k+1]) != Brackets.CloseBracket and type(self.nodeList[k+1]) != Or.Or :
					self.nodeList[k] = Cat.Cat(left=self.nodeList[k], right=self.nodeList[k+1])
					self.nodeList.remove(self.nodeList[k+1])
					end -= 1
					k-=1
				k += 1
			k=start+1
			while k < end:
				if type(self.nodeList[k]) == Or.Or:
					self.nodeList[k] = Or.Or(left=self.nodeList[k-1], right=self.nodeList[k + 1])
					self.nodeList.remove(self.nodeList[k + 1])
					self.nodeList.remove(self.nodeList[k - 1])
					k -= 1
					end -= 2
				k+=1
			if end - start == 2 and flag:
				self.groupList[len(self.groupList)-1].child = self.nodeList[start + 1]
				self.nodeList[start] = self.groupList[len(self.groupList)-1]
				self.nodeList.remove(self.nodeList[start + 1])
				self.nodeList.remove(self.nodeList[start + 1])
			else:
				self.nodeList[start] = self.nodeList[start + 1]
				self.nodeList.remove(self.nodeList[start + 1])
				self.nodeList.remove(self.nodeList[start + 1])
			self.bracketsList.remove(self.bracketsList[i])

	def printSubTreeUnary(self, node, k):
		space = " " * k
		if type(node) == Group.Group:
			print(space +"Group " + str(node.num))
			return node.child
		if type(node) == Clini.Clini:
			print(space +"...")
			return node.child
		if type(node) == Repeat.Repeat:
			print(space +"{} " + str(node.amount))
			return node.child
		if type(node) == SquareBrackets.SquareBrackets:
			print(space +"[] ")
			i=0
			while i < len(node.child):
				print(space +node.child[i].val)
				i+=1
			return None
		if type(node) == Leaf.Leaf:
			if node.val == '':
				print(space + '$')
			else:
				print(space +node.val)
			return None
	def printSubTreeBinary(self, node, k):
		space = " " * k
		if type(node) == Or.Or:
			print(space + "|")
			return (node.left, node.right)
		if type(node) == Cat.Cat:
			print(space + ".")
			return (node.left, node.right)
	def printTree(self, node, k):
		k+=4
		if type(node) != Or.Or and type(node) != Cat.Cat:
			tmp=self.printSubTreeUnary(node, k)
		else:
			tmp=self.printSubTreeBinary(node, k)
		if tmp == None:
			return 0
		if type(tmp) != tuple:
			self.printTree(tmp,k)
		else:
			self.printTree(tmp[0], k)
			self.printTree(tmp[1], k)
	def createNFA(self):
		k=0
		l=[]
		l.append(k)
		self.nodeList[0].makeNFA(True, False, l)
		return self
	def printNFA(self, node, k):
			k += 4
			flag = False
			space = " "*k
			if type(node) == Group.Group:
				tmp = self.printNFA(node.child, k)
				return 0
			if type(node) == NFA.NFA:
				i=0
				print(space+node.nodeName)
				print(node.transitions)
				print(node.start)
				print(node.end)
				for x in self.autoNode:
					if x == node.nodeName:
						flag = True
				self.autoNode.add(node.nodeName)
				while i < len(node.NFAchildren):
					if flag == False:
						self.printNFA(node.NFAchildren[i], k)
						i+=1
					else:
						i+=1
			else:
				self.printNFA(node.startnode, k)
