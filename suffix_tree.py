#TODO : code -> no change in AP when Rule1 ... like the video
END = {'val': None}

class SuffixTree:

	def __init__(self, string):
		self.root = Node(string)
		self.rsc = 0
		self.string = string
		self.activePoint = {'activeNode': self.root, 'activeEdge': None, 'activeLength':0}

	def createSuffixTree(self):
		for i,v in enumerate(self.string):
			END['val'] = i
			self.rsc += 1
			lastNewNode = None
			ext = 0
			while(self.rsc > 0):
				ext+=1
				ae = self.activePoint['activeEdge']
				if ae:
					ae = self.string[ae]
				
				if (self.activePoint['activeLength'] == 0):
					self.activePoint['activeEdge'] = i

				activeEdgeChar = self.string[self.activePoint['activeEdge']]
				self.doWalkDown(activeEdgeChar)
				activeEdgeChar = self.string[self.activePoint['activeEdge']]
				child = self.activePoint['activeNode'].child[ord(activeEdgeChar)]
				if (child):
					# Rule 3
					if ( v == self.string[child.start + self.activePoint['activeLength']] and (child.start + self.activePoint['activeLength'] <= child.end['val']) ) :
						self.activePoint['activeLength'] += 1
						self.addSuffixLink1(lastNewNode)
						lastNewNode = None
						break
					# Rule 2
					else :
						newNode = self.splitNode(child, i)
						newNode.suffix_link = self.root
						self.addSuffixLink2(lastNewNode ,newNode)
						lastNewNode = newNode
						if (self.activePoint['activeNode'] == self.root and self.activePoint['activeLength'] > 0) :
							self.activePoint['activeLength'] -= 1
							self.activePoint['activeEdge'] += 1
							# self.activePoint['activeEdge'] = i - self.rsc -1
						elif (self.activePoint['activeNode'] != self.root) :
							self.activePoint['activeNode'] = self.activePoint['activeNode'].suffix_link
				else :
					# Rule 1
					node = Node(self.string, i)
					self.activePoint['activeNode'].child[ord(v)] = node
					self.addSuffixLink1(lastNewNode)
					lastNewNode = None
				self.rsc -= 1
		return self.root

	def doWalkDown(self, activeEdgeChar):
		child = self.activePoint['activeNode'].child[ord(activeEdgeChar)]
		if (child and self.isInternalNode(child)) :
			edgeLen = child.end['val'] - child.start + 1
			if (edgeLen <= self.activePoint['activeLength']) :
				self.activePoint['activeNode'] = child
				self.activePoint['activeEdge'] += edgeLen
				self.activePoint['activeLength'] -= edgeLen
				activeEdgeChar = self.string[self.activePoint['activeEdge']]
				self.doWalkDown(activeEdgeChar)
			else :
				return
		return


	def splitNode(self, child, i):
		n1 = Node(self.string, child.start, child.start + self.activePoint['activeLength'] - 1 )
		child.start = child.start + self.activePoint['activeLength']
		
		activeEdgeChar = self.string[self.activePoint['activeEdge']]
		self.activePoint['activeNode'].child[ord(activeEdgeChar)] = n1
		
		n1.child[ord(self.string[child.start])] = child

		n2 = Node(self.string, i)
		n1.child[ord(self.string[i])] = n2
		return n1


	def addSuffixLink1(self,lastNewNode):
		if (lastNewNode != None):
			lastNewNode.suffix_link = self.activePoint['activeNode']


	def addSuffixLink2(self, lastNewNode ,newNode):
		if (lastNewNode != None):
			lastNewNode.suffix_link = newNode

	def isRoot():
		pass

	def isLeaf():
		pass

	def isInternalNode(self, node):
		if (node.end['val'] != END['val'] and node.start != None):
			return True
		return False

	def isEdge():
		pass


class Node:

	def __init__(self, string, start=None, end=None):
		self.child = []
		for i in range(256):
			self.child.append(None)
		self.start = start
		if end:
			self.end = {'val':end}
		else:
			self.end = END
		self.string = string
		self.suffix_link = None
		self.suffix_idx = None

def dfs(node, s, a):
	for i, v in enumerate(node.child):
		if(v):
			# print v.start, v.end['val']
			print a+s[v.start:v.end['val']+1]
			dfs(v,s,a+s[v.start:v.end['val']+1])

def ptspace(n):
	for i in range(n) :
		print ' ',

#Create suffix tree in Linear Time

t = SuffixTree('xyzxyaxyz$')
root=t.createSuffixTree()
# for i, v in enumerate(root.child):
# 	if (v):
# 		print chr(i) ,v.start
dfs(root,'xyzxyaxyz$', '->' )