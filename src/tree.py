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
	def volume(self):
		"""Returns the volume of the bound, or the product of the feature bound sizes"""
		vol = 1.0
		maxvol = 1.0
		for b in self.bounds:
			vol = vol*( b[1]-b[0] + 1)
			maxvol = maxvol * (self.max_value+1)
		return vol/maxvol
	def show(self):
		"""Prints the bouding box on the standard output"""
		print 'Bounds:',
		for b in self.bounds:
			print '[',b[0],',',b[1],']',
		print 'vol:',self.volume()

class Tree:
	def __init__(self,feature_count,feature_index,max_value,feature_value,level):
		self.left = None
		self.right = None
		self.samples = []
		self.bounds  = Bounds(feature_count,max_value)
		self.feature_count = feature_count	#the number of features that this three can sort
		self.feature_index = feature_index	#the feature splitten at this level
		self.feature_value = feature_value	#the  subtree on the left have values for feature_index < feature_value, >= on the right
		self.max_value = max_value
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
	def insert_sample(self,sample,level_count,bounds,random = True):
		self.samples.append(sample)
		self.bounds = bounds;
		if(self.level >= level_count -1):
			return
		if(sample.feature[self.feature_index] < self.feature_value):
			if(self.left):
				b = self.left.bounds
				self.left.insert_sample(sample,level_count,b)
			else:
				feature = randint(0,self.feature_count-1)
				value = 0
				if(self.bounds.size(feature) < 2):
					return
				elif(self.bounds.size(feature) == 2):
					value = 1;
				elif(random):
					value = randint(self.bounds.getMin(feature)+1,
								self.bounds.getMax(feature))
				else:
					value = int(self.bounds.getMin(feature) + self.bounds.getMax(feature))/2
				self.left = Tree(self.feature_count,feature,self.max_value,value,self.level + 1)
				b = self.bounds.dup()
				b.setMax(self.feature_index,self.feature_value -1)
				self.left.insert_sample(sample,level_count,b)
		else:
			if(self.right):
				b = self.right.bounds
				self.right.insert_sample(sample,level_count,b)
			else:
				feature = randint(0,self.feature_count-1)
				value = 0
				if(self.bounds.size(feature) < 2):
					return
				elif(self.bounds.size(feature) == 2):
					value = 1;
				elif(random):
					value = randint(self.bounds.getMin(feature)+1,
								self.bounds.getMax(feature))
				else:
					value = int(self.bounds.getMin(feature) + self.bounds.getMax(feature))/2
				self.right = Tree(self.feature_count,feature,self.max_value,value,self.level + 1)
				b = self.bounds.dup()
				b.setMin(self.feature_index,self.feature_value)
				self.right.insert_sample(sample,level_count,b)
	def insertSample(self,sample,level_count,random = True):
		self.insert_sample(sample,level_count,self.bounds,random)
	def getHiClass(self,sample):
		if(self.left == None and self.right == None):
			return self
		if(sample.feature[self.feature_index] < self.feature_value):
			if(self.left and self.left.getSize() > 0):
				return self.left.getHiClass(sample)
			else:
				return self
		else:
			if(self.right and self.right.getSize() > 0):
				return self.right.getHiClass(sample)
			else:
				return self
	def getSize(self,first = 0, last = -1):
		if(last < first):
			return len(self.samples)
		else:
			return len(self.getSamples(first,last))
	def getDensity(self,first = 0, last = -1):
		size = float(self.getSize(first,last) - 1.0)
		if(size > 0.0):
			return size/float(self.bounds.getVolume())
		else:
			return 0.0
	def getSamples(self,first,last):
		return [ x for x in self.samples if (x.frame >= first and x.frame <= last)] 
	def isLeaf(self):
		return self.left == None and self.right == None
	def getLeaves(self):
		if self.left != None and self.right != None:
			A = self.left.getLeaves()
			B = self.right.getLeaves()
			A.extend(B)
			return A
		elif self.left != None:
			return self.left.getLeaves()
		elif self.right != None:
			return self.right.getLeaves()
		else:
			return [self]
	def getLeafSizes(self,first = 0, last = -1):
		leafsizes = []
		for leaf in self.getLeaves():
			size = leaf.getSize(first,last)
			if size > 0 :
				leafsizes.append(size)
		return leafsizes
	def getLeafDensities(self,first = 0, last = -1):
		leafdensities = []
		totalvolume = 0.0
		for leaf in self.getLeaves():
			size = leaf.getSize(first,last)
			if(size > 1):
				totalvolume += leaf.bounds.volume()
				leafdensities.append((size-1)/float(leaf.bounds.volume()))
			else:
				leafdensities.append(0.0)
				#continue
		leafdensities = [ leaf * totalvolume for leaf in leafdensities]
		return leafdensities
	def getEntropy(self,first = 0, last = -1):
		size	  = float(len(self.samples))
		leafsizes = self.getLeafSizes(first,last)
		H = 0.0
		if(size == 0.0):
			return 1
		for leaf in leafsizes:
			if leaf == 0:
				continue
			else:
				H += -(leaf/size)*log(leaf/size,2)
		return H
	def getDensityEntropy(self,first = 0, last = -1):
		leafdensity = self.getLeafDensities(first,last)
		density = float(sum(leafdensity));
		H = 0.0
		if(density == 0.0):
			return 1
		for leaf in leafdensity:
			if leaf == 0.0:
				continue
			else:
				H += -(leaf/density)*log(leaf/density,2)
		return H
	def isSampleBG(self,sample,first = 0, last = -1):
		leaf_size = self.getLeafSizes(first,last)
		sample_class = tree.getHiClass(sample)
		mean = float(sum(leaf_size))/float(len(leaf_size))
		if(sample_class.getSize(first,last) >= mean):
			return True
		else:
			return False
	def isSampleBG2(self,sample,first = 0,last =-1):
		leaf_density = self.getDensities(first,last)
		sample_class = tree.getHiClass(sample)
		mean = float(sum(leaf_density))/float(len(leaf_size))
		if(sample_class.getDensity(first,last) >= mean):
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
			self.trees.append(Tree(feature_count,random(0,feature_count-1),max_value,random(0,max_value),0))
	def insertSample(self,sample):
		for t in self.trees:
			t.insertSample(sample,self.level_count)
	def isSampleBG(self,sample):
		votes = 0
		for t in self.trees:
			if(t.isSampleBG(sample)):
				votes = votes + 1
		return float(votes)/float(len(self.trees))
	def isSampleBG2(self,sample):
		votes = 0
		for t in self.trees:
			if(t.isSampleBG2(sample)):
				votes = votes + 1
		return float(votes)/float(len(self.trees))

def sample_new_random(feature_count,max_value,frame = 0):
	return Sample([randint(0,max_value) for x in range(0,feature_count)],frame)

def main():
	print "yo"
	t = Tree(3,1,255,128,0)
	for x in range(0,400):
		s = sample_new_random(3,255)
		t.insertSample(s,10,True)
	
	#s = Sample([6,6,6])
	#t.insertSample(s,5)
	#t.insertSample(s,5)
	#t.insertSample(s,5)
	#s = Sample([254,255,250])
	#t.insertSample(s,5)
	#t.showAll()
	print t.getLeafSizes()
	print t.getLeafDensities()
	print t.getEntropy()
	print t.getDensityEntropy()
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
# - read/write a video / sequence of images
# - make the tree grow lazily : done
# - make the tree grow with a maximum / minimum size
# - compute entropy on densities instead of sizes.

