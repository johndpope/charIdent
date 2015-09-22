import cPickle as pickle
from datapoint import Datapoint
import os

class Dataset:
	def __init__(self, dest_dir):
		self.darray = []
		for i in range(62):
			self.darray.append([])
		self.dest_dir = dest_dir

	def addImage(self, image, count, char_type, char_index):
		d = Datapoint(image, count, char_type)
		self.darray[char_index].append(d)

	def indextochar(self, index):
		if(index < 26):
			return chr(ord('A') + index)
		if(index < 52):
			return chr(ord('a') + index - 26)
		return chr(ord('0') + index - 52)

	def saveDataset(self):
		for i in range(62):
			if(i < 26):
				char_type = chr(ord('A') + i)
			elif(i < 52):
				char_type = chr(ord('a') + i - 26)
			else:
				char_type = chr(ord('0') + i - 52)
			out_file_name = 'char_' + char_type + '.pkl'
			out_file_path = os.path.join(self.dest_dir, out_file_name)
			fout = open(out_file_path, 'wb')
			pickle.dump(self.darray[i], fout, pickle.HIGHEST_PROTOCOL)
			print str(char_type) + ' -------------> ' + str(len(self.darray[i])) + ' datapoints.'

	def loadDataset(self):
		for i in range(62):
			if(i < 26):
				char_type = chr(ord('A') + i)
			elif(i < 52):
				char_type = chr(ord('a') + i - 26)
			else:
				char_type = chr(ord('0') + i - 52)
			out_file_name = 'char_' + char_type + '.pkl'
			out_file_path = os.path.join(self.dest_dir, out_file_name)
			self.darray[i] = pickle.load(open(out_file_path, 'rb'))

