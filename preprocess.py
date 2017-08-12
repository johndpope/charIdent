from PIL import Image
import PIL.ImageOps
# import cv2
import os
from dataset import Dataset
from progressbar import *
import time

class Preprocess:

	def __init__(self):
		self.source_dir = ["../mlp-character-recognition/dataset"] #, "../sd_nineteen/HSF_1", "../sd_nineteen/HSF_2"]
		self.dest_dir = "./dataset"
		self.char_count = []
		for i in range(62):
			self.char_count.append(0)
		self.width = 28
		self.height = 28
		self.resize_op = Image.ANTIALIAS
		self.dset = Dataset(self.dest_dir)

	def preprocessImage(self, file_name):
		name = os.path.basename(file_name)
		# start = name.find('_')
		# n = 6
		# while start > 0 and n > 0:
		# 	start = name.find('_', start + 1)
		# 	n -= 1
		# char_type = name[start + 1]
		char_type = name[0]
		char_type = ord(char_type)
		if(char_type >= ord('A') and char_type <= ord('Z')):
			char_index = char_type - ord('A') + 26
		elif(char_type >= ord('a') and char_type <= ord('z')):
			char_index = char_type - ord('a')
		else:
			char_index = char_type - ord('0') + 52
		self.char_count[char_index] += 1
		# img = cv2.imread(file_name)
		# img[img == 255] = 1
		# img[img == 0] = 255
		# img[img == 1] = 0
		# img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		# ret,thresh = cv2.threshold(img,127,255,0)
		# contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		# cnt = contours[0]
		# x,y,w,h = cv2.boundingRect(cnt)
		# dim = max(w,h)
		# letter = img[max(0,y-5):min(y+dim+5,127),max(0,x-5):min(x+dim+5,127)]
		# letter = cv2.resize(letter, (self.width, self.height))
		im = Image.open(file_name)
		if (im.mode == 'RGBA'):
			r,g,b,a = im.split()
			im = Image.merge('RGB', (r,g,b))
		# im = im.crop((max(0,y-5),min(y+dim+5,127),max(0,x-5),min(x+dim+5,127)))
		# im = im.resize((self.width, self.height), self.resize_op)
		im = PIL.ImageOps.invert(im)
		self.dset.addImage(im, self.char_count[char_index], chr(char_type), char_index)

	def preprocessDirectory(self):
		cnt = 1
		for d in self.source_dir:
			self.subdir = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
			dir_str = 'Directory %d of %d: ' % (cnt, len(self.source_dir))
			widgets=[dir_str, Bar('=', '[', ']'), ' ', Percentage(), ' ', ETA(), ' ', FileTransferSpeed()]
			bar = ProgressBar(maxval=len(self.subdir), widgets=widgets).start()
			for i in range(len(self.subdir)):
				sdir = self.subdir[i]
				imfile = [os.path.join(sdir,f) for f in os.listdir(sdir) if os.path.isfile(os.path.join(sdir,f))]
				for f in imfile:
					if(f.endswith('.png')):
						self.preprocessImage(f)
				bar.update(i + 1)
			bar.finish()
			cnt += 1
		self.dset.saveDataset()