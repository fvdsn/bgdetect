import Image
from math import sqrt

class Ima :
	
	
	def __init__(self, image) :
		
		im = Image.open(image)
		self.mode = im.mode
		self.width = im.size[0]
		self.height = im.size[1]
		self.data = list(im.getdata())
		self.x = {}
		self.x[(0,0)] = 1
		self.x[(1,0)] = 2
		self.x[(2,0)] = 1
		self.x[(0,1)] = 0
		self.x[(1,1)] = 0
		self.x[(2,1)] = 0
		self.x[(0,2)] = -1
		self.x[(1,2)] = -2
		self.x[(2,2)] = -1
		
		self.y = {}
		self.y[(0,0)] = 1
		self.y[(0,1)] = 2
		self.y[(0,2)] = 1
		self.y[(1,0)] = 0
		self.y[(1,1)] = 0
		self.y[(1,2)] = 0
		self.y[(2,0)] = -1
		self.y[(2,1)] = -2
		self.y[(2,2)] = -1
		print self.x
		print self.y

	""" 
		Params : coord : un tuple (x,y)
	"""
	def getPixel(self,coord) :
		if(coord[0] >= self.width or coord[0] < 0 or coord[1] >= self.height or coord[1] < 0) :
			return (0,0,0)
		else :				
			return self.data[coord[1] * self.width + coord[0]]
		
	def gradimage(self, image) :
		imNew=Image.new(self.mode ,(self.width, self.height)) 
		imNew.putdata(self.gradient()) 
		imNew.save(image)

		
	def gradient(self) :
		self.gr = []
		for j in xrange(0, self.height) :
			for i in xrange(0, self.width) :
				self.gr.append(self.grad((i, j)))
			

		return self.gr
		
		
	def grad(self, coord) :
		x = self.gx(coord)
		y = self.gy(coord)
		g1 = sqrt(x[0] * x[0] + y[0] * y[0])
		g2 = sqrt(x[1] * x[1] + y[1] * y[1])
		g3 = sqrt(x[2] * x[2] + y[2] * y[2])
		return (int(g1 * 255 / 1081 ), int(g2 * 255 / 1081), int(g3 * 255 / 1081))
		
	def gx(self, coord) :
		return self.g(coord, self.x)
		
		
	def gy(self, coord) :
		return self.g(coord, self.y)
				
	def g(self, coord, op) : 
		sum1 = 0
		sum2 = 0
		sum3 = 0
		for i in xrange(-1, 2) :
			for j in xrange(-1 , 2) :
				sum1 += op[(i + 1,j + 1)] * self.getPixel((coord[0] + i, coord[1] + j))[0]
				sum2 += op[(i + 1,j + 1)] * self.getPixel((coord[0] + i, coord[1] + j))[1]
				sum3 += op[(i + 1,j + 1)] * self.getPixel((coord[0] + i, coord[1] + j))[2]
				
		return (sum1, sum2, sum3)
		

i = Ima("test/1.jpg")
#print i.getPixel((0,-1))
#print i.gx((1,1))
#print i.gy((1,1))
#print i.grad((1,1))
#print i.gradient()
i.gradimage("grad2.jpg")
