class UF :
	
	id_arr = []
	size = []

	def __init__(self, n):
		self.id_arr = [i for i in range(0,n)] 
		self.size = [1 for i in range(0,n)]      # save size of tree root at the id (only where id is root)

	def root(self, x):
		# Finding root and recursively balancing tree
		if x != self.id_arr[x] :
			r = self.root(self.id_arr[x])
			return r
		return x

	def union(self, a, b) :
		# union with connecting smaller tree with bigger
		# size is number of nodes not the depth of the tree
		r_a = self.root(a)
		r_b = self.root(b)
		if(self.size[r_a] < self.size[r_b]) :
			self.id_arr[r_a] = r_b
			self.size[r_b] += self.size[r_a]
		else:
			self.id_arr[r_b] = r_a
			self.size[r_a] += self.size[r_b]

	def find(self, x, y):
		return True if self.root(x)==self.root(y) else False


n = int(raw_input())
obj = UF(n)

while(True):
	try:
		try:
			c_input = raw_input().split()
		except(EOFError):
			break
		operation, a, b = c_input[0], int(c_input[1]), int(c_input[2])
		if operation == 'u' :
			obj.union(a,b)
		elif operation == 'f' :
			print 'Connected' if obj.find(a,b) else 'Not Connected'
		else:
			raise Exception('not a valid operation')

	except Exception as e:
		print 'Exception -> \t' , e