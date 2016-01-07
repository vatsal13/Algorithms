# a = [1,2,3,4,5]
# import kth_largest
# kth_largest.klargest(a,3)

def mean5(A) :
	A.sort()
	return A[len(A)/2]

def mom(A) :
	mean_arr = []
	print A
	for i in range(0,len(A),5):
		end = len(A) if i+5 > len(A) else i+5
		mean_arr.append(mean5(A[i:end+1]))

	print 'here',mean_arr,len(mean_arr),len(mean_arr)/2
	if (len(mean_arr)<=5):
		return mean5(mean_arr)
	return klargest(mean_arr,len(mean_arr)/2)	

def partition(A, approx_median) :
	a1 = []
	a2 = []
	dup = 0
	median_indx = 0
	for idx, val in enumerate(A) :
		if dup < 1 and val == approx_median :
			dup += 1
		elif val < approx_median :
			a1.append(val)
			median_indx +=1	
		elif val >= approx_median :
			a2.append(val)

	return [a1,a2,median_indx]


def klargest(A, k):
	if k > len(A):
		return False

	print A
	approx_median = mom(A)
	print 'median is : ' , approx_median

	res = partition(A, approx_median)
	a1, a2, median_indx = res[0], res[1], res[2]
	print "a1, a2, median_indx", res[0], res[1], res[2]
	if k == median_indx :
		print "===============================================================",A,approx_median
		return approx_median
	elif k > median_indx :
		print 'looking for' , k-median_indx-1
		return klargest(a2, k-median_indx-1)
	elif k < median_indx :
		print 'looking for' , k
		return klargest(a1, k)








