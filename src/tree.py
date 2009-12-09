#!/usr/bin/python
from random import *
from numpy import *
from math import *

# A sample represents a pixel in one frame
# sample feature is a vector of integers representing it's data
# the sample feature vector can be its r g b components but also it's gradient
# or other information
class Sample:
	def __init__(self,feature,frame = 0 ):
		""" Creates a new Sample
		feature -- List - the feature vector
		frame -- Int -- the movie frame where the sample was taken """ 
		self.feature_count = len(feature)
		self.feature = feature
		self.frame = frame
	def getLength(self):	
		""" Returns the length of the feature vector """
		return len(self.feature)

class Bounds:
	def __init__(self,feature_count,max_value):
		"""Creates a new Bounding box around feature values
		feature_count -- Int -- The length of the feature vectors
		max_value -- The values of the feature vector will be in [0,max_value]"""
		self.feature_count = feature_count
		self.max_value = max_value
		self.bounds = zeros((feature_count,2)) #bounds[f][0] is lower inclusive bound for feature f, #bounds[f][1] is higher inclusive bound for feature f
		#initializing bounds to [0,max_value] for all features.
		for b in self.bounds :
			b[0] = 0
			b[1] = max_value
	def setBound(self,feature,min,max):
		self.bounds[feature][0] = min
		self.bounds[feature][1] = max
	def setMin(self,feature,min):
		self.bounds[feature][0] = min
	def setMax(self,feature,max):
		self.bounds[feature][1] = max
	def getMin(self,feature):
		return self.bounds[feature][0]
	def getMax(self,feature):
		return self.bounds[feature][1]
	def copy(self,bounds):
		"""Copy a Bounds into this one
		bounds -- Bounds -- The bound that will be copied into self"""
		i = self.feature_count
		while(i):
			i = i-1
			self.bounds[i][0] = bounds.bounds[i][0]
			self.bounds[i][1] = bounds.bounds[i][1]
	def dup(self):
		"""Creates a duplicate object of self"""
		b = Bounds(self.feature_count,self.max_value)
		b.copy(self)
		return b
	def size(self,feature):
		"""Returns the count of different values inside the bounds for a single feature of the feature vector"""
		return self.bounds[feature][1]-self.bounds[feature][0] + 1
	def show(self):
		"""Prints the bouding box on the standard output"""
		print 'Bounds:',
		for b in self.bounds:
			print '[',b[0],',',b[1],']',
		print ''

class Tree:
	def __init__(self,feature_count,feature_index,max_value,feature_value,level):
		self.left = None
		self.right = None
		self.samples = []
		self.bounds  = Bounds(feature_count,max_value)
		self.feature_count = feature_count	#the number of features that this three can sort
		self.feature_index = feature_index	#the feature splitten at this level
		self.feature_value = feature_value	#the  subtree on the left have values for feature_index < feature_value, >= on the right
		self.level = level
	def setLeft(self,left):
		self.left = left
	def setRight(self,right):
		self.right = right
	def getLeft(self):
		return self.left
	def getRight(self):
		return self.right
	def getBounds(self):
		return self.bounds
	def setBounds(self,bounds):
		self.bounds = bounds.dup()
	def addSample(self,sample):
		self.samples.append(sample)
		if(sample.feature[self.feature_index] < self.feature_value):
			if(self.left):
				self.left.addSample(sample)
		else:
			if(self.right):
				self.right.addSample(sample)
	def insertSample(self,sample,level_count):
		self.samples.append(sample)
		if(self.level >= level_count -1):
			return
		if(sample.feature[self.feature_index] < self.feature_value):
			if(self.left):
				self.left.insertSample(sample,level_count)
			else:
				feature = randint(0,self.feature_count-1)
				value = 0
				if(self.bounds.size(feature) < 2):
					return
				elif(self.bounds.size(feature) == 2):
					value = 1;
				else:
					value = randint(self.bounds.getMin(feature)+1,
								self.bounds.getMax(feature))
				self.left = Tree(self.feature_count,feature,self.max_value,value,self.level + 1)
				b = self.bounds.dup()
				b.setMax(self.feature_index,self.feature_value -1)
				self.left.insertSample(sample,level_count)
		else:
			if(self.right):
				self.right.insertSample(sample,level_count)
			else:
				feature = randint(0,self.feature_count-1)
				value = 0
				if(self.bounds.size(feature) < 2):
					return
				elif(self.bounds.size(feature) == 2):
					value = 1;
				else:
					value = randint(self.bounds.getMin(feature)+1,
								self.bounds.getMax(feature))
				self.right = Tree(self.feature_count,feature,self.max_value,value,self.level + 1)
				b = self.bounds.dup()
				b.setMin(self.feature_index,self.feature_value)
				self.right.insertSample(sample,level_count)



			
	def getDeepClass(self,sample):
		if(self.left == None and self.right == None):
			return (self.samples,self.level)
		if(sample.feature[self.feature_index] < self.feature_value):
			if(self.left):
				return self.left.getDeepClass(sample)
			else:
				return ([],self.level)
		else:
			if(self.right):
				return self.right.getDeepClass(sample)
			else:
				return ([],self.level)
	def getHiClass(self,sample):
		if(self.left == None and self.right == None):
			return (self.samples,self.level)
		if(sample.feature[self.feature_index] < self.feature_value):
			if(self.left and self.left.getSize > 0):
				return self.left.getHiClass(sample)
			else:
				return (self.samples,self.level)
		else:
			if(self.right and self.right.getSize > 0):
				return self.right.getHiClass(sample)
			else:
				return (self.samples,self.level)
	def getSize(self):
		return len(self.samples)
	def isLeaf(self):
		return self.left == None and self.right == None
	def getLeafSizes(self):
		if len(self.samples) == 0:
			return []
		if self.left != None and self.right != None:
			A = self.left.getLeafSizes()
			B = self.right.getLeafSizes()
			A.extend(B)
			return A
		elif self.left != None :
			return self.left.getLeafSizes()
		elif self.right != None :
			return self.right.getLeafSizes()
		else:
			return [len(self.samples)]
	def getEntropy(self):
		size	  = float(len(self.samples))
		leafsizes = self.getLeafSizes()
		H = 0.0
		if(size == 0.0):
			return 1
		for leaf in leafsizes:
			if leaf == 0:
				continue
			else:
				H += -(leaf/size)*log(leaf/size,2)
		return H
	def isSampleBG(self,sample):
		leaf_size = self.getLeafSizes()
		sample_class = tree.getHiClass(sample)
		mean = float(sum(leaf_size))/float(len(leaf_size))
		if(len(sample_class) >= mean):
			return True
		else:
			return False
	def show(self):
		i = self.level
		while(i):
			i = i-1
			print ' ',
		print 'Tree: fi:',self.feature_index,'fv:',self.feature_value,'->',len(self.samples)
		i = self.level
		while(i):
			i = i-1
			print ' ',
		self.bounds.show()
	def showAll(self):
		self.show()
		if(self.left):
			self.left.showAll()
		if(self.right):
			self.right.showAll()

def tree_new_random_rec(bounds,feature_count,max_value,level,level_count):
	if(level >= level_count):
		return None
	feature = randint(0,feature_count -1)
	if(bounds.size(feature) >= 2):
		value = 0
		if(bounds.size(feature) == 2):
			value = 1
		else:
			value = random.randint(bounds.getMin(feature)+1, bounds.getMax(feature))
		t = Tree(feature_count,feature,max_value,value,level)
		t.setBounds(bounds)
		bl = bounds.dup()
		bl.setMax(feature,value -1)
		br = bounds.dup()
		br.setMin(feature,value)
		t.setLeft(tree_new_random_rec(bl,feature_count,max_value,level+1,level_count))
		t.setRight(tree_new_random_rec(br,feature_count,max_value,level+1,level_count))
		return t
	else:
		return Tree(feature_count,0,max_value,0,level)

def tree_new_random(feature_count,max_value,level_count):
	b = Bounds(feature_count,max_value)
	return tree_new_random_rec(b,feature_count,max_value,0,level_count)

class TreeSet:
	def __init__(self,tree_count,feature_count,max_value,level_count):
		self.tree_count = tree_count
		self.feature_count = feature_count
		self.max_value = max_value
		self.level_count = level_count
		self.trees = []
		i = tree_count
		while(i):
			i = i - 1
			self.trees.append(tree_new_random(feature_count,max_value,level_count))
	def addSample(self,sample):
		for t in self.trees:
			t.addSample(sample)
	def isSampleBG(self,sample):
		votes = 0
		for t in self.trees:
			if(t.isSampleBG(sample)):
				votes = votes + 1
		return float(votes)/float(len(self.trees))

def main():
	print "yo"
	t = tree_new_random(3,255,5)
	s = Sample([6,6,6])
	t.addSample(s)
	t.addSample(s)
	t.addSample(s)
	s = Sample([66,66,66])
	t.addSample(s)
	t.showAll()
	print t.getLeafSizes()
	print t.getEntropy()
	return 0

if __name__ == "__main__":
	main()

# TODO LIST
# - use a time window to use frame close to a point
# - how to choose good trees : good entropy ? good entropy in frame window ?
# - how to decide if a sample is bg or not ?
#	- look only at leaves
#	- look at whole tree
#	- how does the size of class correlates to the likelyness to belong to the bg.
# - read a video
# - make the tree grow lazily

