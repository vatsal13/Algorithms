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
			print '\n ++++++++++++++ Phase ',i,' --- ', self.string , 'char  - ', v
			END['val'] = i
			print 'END = ',i
			self.rsc += 1
			print 'RSC = ',self.rsc
			lastNewNode = None
			if lastNewNode:
				print 'Last-New-Node = [',lastNewNode.start, lastNewNode.end['val'],']'
			else:
				print 'Last-New-Node = None'
			ext = 0
			while(self.rsc > 0):
				ext+=1
				print ' ------------------Extension e --- ', ext

				ae = self.activePoint['activeEdge']
				if ae:
					ae = self.string[ae]
				print '\t AP = ([',self.activePoint['activeNode'].start,',', self.activePoint['activeNode'].end['val'],'], ', ae, self.activePoint['activeEdge'] ,', ',self.activePoint['activeLength'],')'
				
				if (self.activePoint['activeLength'] == 0):
					print '\tActive Length = 0  So, '
					self.activePoint['activeEdge'] = i
					print '\t AP = ([',self.activePoint['activeNode'].start,',', self.activePoint['activeNode'].end['val'],'], ', self.string[self.activePoint['activeEdge']], self.activePoint['activeEdge'] ,', ',self.activePoint['activeLength'],')'

				activeEdgeChar = self.string[self.activePoint['activeEdge']]
				self.doWalkDown(activeEdgeChar)
				activeEdgeChar = self.string[self.activePoint['activeEdge']]
				# print self.activePoint, self.activePoint['activeNode'].start
				child = self.activePoint['activeNode'].child[ord(activeEdgeChar)]
				if (child):
					# Rule 3
					print '\t Edge exists from Active Node'
					if ( v == self.string[child.start + self.activePoint['activeLength']] and (child.start + self.activePoint['activeLength'] <= child.end['val']) ) :
						print '\t-----Rule 3-----'
						self.activePoint['activeLength'] += 1
						print '\t AP = ([',self.activePoint['activeNode'].start,',', self.activePoint['activeNode'].end['val'],'], ', self.string[self.activePoint['activeEdge']],self.activePoint['activeEdge'] ,', ',self.activePoint['activeLength'],')'
						self.addSuffixLink1(lastNewNode)
						lastNewNode = None
						break
					# Rule 2
					else :
						print '\t -----Rule 2-----'
						newNode = self.splitNode(child, i)
						newNode.suffix_link = self.root
						print '\t >>>> Making a suffix_link from newNode [', newNode.start,',',newNode.end['val'],'] to Root'
						if lastNewNode:
							print '\tLast-New-Node = [',lastNewNode.start, lastNewNode.end['val'],']'
						else:
							print '\tLast-New-Node = None'
						self.addSuffixLink2(lastNewNode ,newNode)
						lastNewNode = newNode
						if (self.activePoint['activeNode'] == self.root and self.activePoint['activeLength'] > 0) :
							print '\t Using 2.1'
							self.activePoint['activeLength'] -= 1
							self.activePoint['activeEdge'] += 1
							# self.activePoint['activeEdge'] = i - self.rsc -1
						elif (self.activePoint['activeNode'] != self.root) :
							print '\t Using 2.2'
							self.activePoint['activeNode'] = self.activePoint['activeNode'].suffix_link
						print '\t AP = ([',self.activePoint['activeNode'].start,',', self.activePoint['activeNode'].end['val'],'], ', self.string[self.activePoint['activeEdge']],self.activePoint['activeEdge'] ,', ',self.activePoint['activeLength'],')'
				else :
					# Rule 1
					print '\t-----Rule 1-----'
					node = Node(self.string, i)
					self.activePoint['activeNode'].child[ord(v)] = node
					self.addSuffixLink1(lastNewNode)
					lastNewNode = None
					print '\t AP = ([',self.activePoint['activeNode'].start,',', self.activePoint['activeNode'].end['val'],'], ', self.string[self.activePoint['activeEdge']],self.activePoint['activeEdge'] ,', ',self.activePoint['activeLength'],')'
				self.rsc -= 1
				print "\tRSC ---------",self.rsc
		print "RSC ---------",self.rsc
		return self.root


	def doWalkDown(self, activeEdgeChar):
		child = self.activePoint['activeNode'].child[ord(activeEdgeChar)]
		if (child and self.isInternalNode(child)) :
			edgeLen = child.end['val'] - child.start + 1
			if (edgeLen <= self.activePoint['activeLength']) :
				print "\t Doing WalkDown :D"
				self.activePoint['activeNode'] = child
				self.activePoint['activeEdge'] += edgeLen
				self.activePoint['activeLength'] -= edgeLen
				activeEdgeChar = self.string[self.activePoint['activeEdge']]
				print '\t AP = ([',self.activePoint['activeNode'].start,',', self.activePoint['activeNode'].end['val'],'], ', self.string[self.activePoint['activeEdge']],self.activePoint['activeEdge'] ,', ',self.activePoint['activeLength'],')'
				self.doWalkDown(activeEdgeChar)
			else :
				return
		return


	def splitNode(self, child, i):
		print '\t **** Spliting Node ****'
		print '\t **** Spliting [', child.start,',', child.end['val'],'] , at ' , child.start + self.activePoint['activeLength']-1
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
			print '\t >>>> Making a suffix_link from newNode [', lastNewNode.start,',',lastNewNode.end['val'],'] to activeNode'


	def addSuffixLink2(self, lastNewNode ,newNode):
		if (lastNewNode != None):
			lastNewNode.suffix_link = newNode
			print '\t >>>> Making a suffix_link from newNode [', lastNewNode.start,',',lastNewNode.end['val'],'] to newNode [', newNode.start,',',newNode.end['val'] ,']'

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

# def dfs(node, s, n):
# 	for i, v in enumerate(node.child):
# 		if(v):
# 			ptspace(n)
# 			# print v.start, v.end['val']
# 			print s[v.start:v.end['val']+1]
# 			n2 = len(s[v.start:v.end['val']+1])
# 			dfs(v,s,n2+n)

def dfs(node, s, a):
	for i, v in enumerate(node.child):
		if(v):
			# print v.start, v.end['val']
			print a+s[v.start:v.end['val']+1]
			dfs(v,s,a+s[v.start:v.end['val']+1])

def ptspace(n):
	for i in range(n) :
		print ' ',



t = SuffixTree('xyzxyaxyz$')
root=t.createSuffixTree()
print root.end
for i, v in enumerate(root.child):
	if (v):
		print chr(i) ,v.start
# for i, v in enumerate(root.child[ord('a')].child[ord('a')].child):
# 	if (v):
# 		print chr(i) ,v.start
print '-----------DFS---------'
dfs(root,'xyzxyaxyz$', '->' )
print '-----------DFS---------'

# for i, v in enumerate(root.child):
# 	if (v):
# 		print chr(i) ,v.start
# print '-------------------- root -> y'
# for i, v in enumerate(root.child[ord('y')].child):
# 	if (v):
# 		print chr(i) ,v.start,v.end
# print '-------------------- y -> z'
# for i, v in enumerate(root.child[ord('y')].child[ord('z')].child):
# 	if (v):
# 		print chr(i) ,v.start,v.end