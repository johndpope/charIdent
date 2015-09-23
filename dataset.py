import cPickle as pickle
from datapoint import Datapoint
import os
import numpy as np
import random

class Dataset:
	def __init__(self, dest_dir):
		self.darray = []
		for i in range(62):
			self.darray.append([])
		self.dest_dir = dest_dir
		# Training dataset partition percentage
		self.perc = 75

	def addImage(self, image, count, char_type, char_index):
		d = Datapoint(image, count, char_type, char_index)
		self.darray[char_index].append(d)

	def indextochar(self, index):
		if(index < 26):
			return chr(ord('A') + index)
		if(index < 52):
			return chr(ord('a') + index - 26)
		return chr(ord('0') + index - 52)

	def saveDataset(self):
		tot_images = 0
		log_file = open(os.path.join(self.dest_dir, 'index.txt'), 'w')
		log_file.write('chr\tnum\n')
		print 'chr\tnum'
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
			tot_images += len(self.darray[i])
			log_file.write(str(char_type) + ' \t ' + str(len(self.darray[i])) + '\n')
			print str(char_type) + '\t' + str(len(self.darray[i]))
		log_file.write(str(tot_images) + ' total images processed.\n')
		print '%d total images processed.' % tot_images
		log_file.close()

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

	def getPartitions(self):
		data_arr = []
		tr_arr = []
		tst_arr = []
		for i in range(62):
			data_arr.extend(self.darray[i])
		random.shuffle(data_arr)
		print 'Found %d images in the dataset' % len(data_arr)
		print 'Splitting dataset into training and test partitions in %d : %d ratio' % (self.perc, 100 - self.perc)
		splidx = int(len(data_arr)*(self.perc/100.0))
		tst_arr = data_arr[:splidx]
		tr_arr = data_arr[splidx:]
		training_inputs = []
		training_results = []
		test_inputs = []
		test_results = []
		for dpoint in tr_arr:
			training_results.append(result_vector(dpoint.char_index))
			training_inputs.append(image_vector(dpoint))
		for dpoint in tst_arr:
			test_results.append(dpoint.char_index)
			test_inputs.append(image_vector(dpoint))
		training_data = zip(training_inputs, training_results)
		test_data = zip(test_inputs, test_results)
		return (training_data, test_data)


	def result_vector(j):
		e = np.zeros((62, 1))
		e[j] = 1.0
		return e

	def image_vector(dpoint):
		e = np.zeros((dpoint.width * dpoint.height, 1))
		for i in range(dpoint.width):
			for j in range(dpoint.height):
				e[i*dpoint.width + j] = dpoint.im[i][j]
		return e
