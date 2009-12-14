#!/usr/bin/env python
#
#       main.py
#       
#       Copyright 2009 mythrys <mythrys@mythrys-laptop>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import os
import jpg
from tree import *

def load(dossier_in) :
	Image = []
	i = 1
	liste = os.listdir(dossier_in)
	liste.sort()
	
	for file in liste:
		print file
		Image.append(jpg.Ima(dossier_in + "/" + file, i))
		i += 1
		print i
	
	
	
		
	
	for j in xrange(0, Image[0].getHeight()) :
			for i in xrange(0, Image[0].getWidth()) :
				treeSet = TreeSet(20, 3, 255, 8)
				for im in Image : 
					s = Sample(im.getSample((i,j)), im.getFrame())
					treeSet.insertSample(s)
		
				for im in Image :
					s = Sample(im.getSample((i,j)), im.getFrame())
					im.setBG((i,j), treeSet.isSampleBG2(s))
					#print treeSet.isSampleBG(s) , " " , im.getFrame()
					
					#print "----"
			print j	
	
	for im in Image :
		coord  = (15,10)
	
		im.save("out")
		
	


def main():
	dossier_in = "imp"
	dossier_out = "out"
	os.system("mkdir out")
	load(dossier_in)
	return 0

if __name__ == '__main__': 
	main()
