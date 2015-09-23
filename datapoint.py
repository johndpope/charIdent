from PIL import Image

class Datapoint:
	def __init__(self, image, count, char_type, char_index):
		(self.width, self.height) = image.size
		self.im = [[0 for x in range(self.width)] for x in range(self.height)] 
		self.imgno = count
		self.char_type = char_type
		self.char_index = char_index
		pix = image.load()
		for i in range(self.width):
			for j in range(self.height):
				(self.im[i][j],_,_) = pix[i,j]
