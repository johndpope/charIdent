from datapoint import Datapoint
import cPickle as pickle
import network
import preprocess
from PIL import Image
import PIL.ImageOps
import numpy as np
from dataset import Dataset

net=pickle.load(open('./network.pkl','rb'))
print net.sizes
ans = []
sumans = 0
char_var = 'o'
char_type = ord(char_var)
if(char_type >= ord('A') and char_type <= ord('Z')):
	char_index = char_type - ord('A') + 26
elif(char_type >= ord('a') and char_type <= ord('z')):
	char_index = char_type - ord('a')
else:
	char_index = char_type - ord('0') + 52
d = Dataset('./dataset')
print 'Loading dataset...',
# d.loadDataset()
for cnt in range(2500):
	print str(cnt) + ' running'
	image_name = str(char_var) + '_' + str(cnt) + '.png'
	image_loc = '../mlp-character-recognition/captcha_images/' + str(char_var) + '/' + image_name
	# image_loc = 'A_0.png'
	print image_loc
	im=Image.open(image_loc) #take file_name as input via function or cmd line
	if (im.mode == 'RGBA'):
		r,g,b,a = im.split()
		im = Image.merge('RGB',(r,g,b))
	im = PIL.ImageOps.invert(im)
	# print im
	# dp = Datapoint(im, 1, 'A', 1)
	width,height = im.size
	image = [[0 for x in range(width)] for x in range(height)]
	pix=im.load()
	for i in range(width):
		for j in range(height):
			(image[i][j],_,_) = pix[i,j]
	a = np.zeros((width * height,1))
	# a = d.image_vector(dp)
	# print a
	for i in range(width):
		for j in range(height):
			a[i*width + j] = image[i][j]/255.0
	# a = d.darray[char_idx - 65 + 26][cnt]
	# a = d.image_vector(a)
	# print a
	ret = net.feedforward(a) 	#ret will contain output vector of size 62
	# print net.weights

	# print ret
	# print np.argmax(ret)
	ans.append(np.argmax(ret))

	arr = [[0 for i in range(2)] for i in range(3)]

	count =0
	for i in ret:
		if ( i > arr[0][0]):
			arr[2] = arr[1]
			arr[1] = arr[0]
			arr[0] = (i,count)
		elif (i > arr[1][0] ):
			arr[2] = arr[1]
			arr[1] = (i,count)
		elif (i > arr[2][0]) :
			arr[2] = (i,count)
		count = count+1	

	#now just need to convert
	for el in arr:
		if(el[1] > 51):
			out = el[1] - 52
		elif (el[1] < 26):
			out = chr(97 + el[1])
		else :
			out = chr(65 + (el[1] - 26))	
		print out
	
# print ans
print sum(i == char_index for i in ans)

