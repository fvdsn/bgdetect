#! /bin/env python

import os

def avi2jpg(input, dossier) :
	os.system("mkdir " + dossier )
	os.system("ffmpeg -i " + input + " -an -r 30 -y " + dossier + "/%d.jpg")
	
	
if __name__ == "__main__":
	avi2jpg("SAM_0440.AVI" , "video")
