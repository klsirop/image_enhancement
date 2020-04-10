from PIL import Image
import numpy as np
import time

def load_image():
	mypic = open("mypic", "r")
	mynames = mypic.read()
	print(mynames)
	filename = raw_input("Choose image:")

	fullname = "./pic/" + filename + ".bmp"
	image = Image.open(fullname)
	new_image = Image.new('L', image.size, 0)
	new_image.paste(image)
	image = new_image
	image.show()
	fullname = "./grey/" + filename + ".bmp"
	image.save(fullname, 'BMP')
	return image, filename


def linear(image, filename):
	im_wid, im_hei = image.size
	image_load = image.load()

	f_min = -1
	f_max = -1
	for j in range(im_hei):
		for i in range(im_wid):
			if (f_min == -1 or image_load[i, j] < f_min):
				f_min = image_load[i, j]
			if (f_max == -1 or image_load[i, j] > f_max):
				f_max = image_load[i, j]

	wish_min = input("Type wish brightness min:")
	wish_max = input("Type wish brightness max:")

	new_arr = np.zeros((im_hei, im_wid), dtype=np.uint8)
	for j in range(im_hei):
		for i in range(im_wid):
			new_arr[j][i] = ((image_load[i, j] - f_min) * (wish_max - wish_min)) / (f_max - f_min) + wish_min

	new_image = Image.fromarray(new_arr)
	new_image.show()
	fullname = "./save/linear/" + filename + "_" + str(wish_min) + "_" + str(wish_max) + ".bmp"
	new_image.save(fullname, 'BMP')


def degree(image, filename):
	im_wid, im_hei = image.size
	image_load = image.load()

	norm_bright = np.zeros((im_hei, im_wid))
	for j in range(im_hei):
		for i in range(im_wid):
			norm_bright[j][i] = float(image_load[i, j]) / 255

	c = input("Type c:")
	f0 = input("Type f0:")
	y = input("Type y:")

	new_arr = np.zeros((im_hei, im_wid))
	for j in range(im_hei):
		for i in range(im_wid):
			new_arr[j, i] = c * ((norm_bright[j, i] + f0) ** y)

	res_arr = np.zeros((im_hei, im_wid), dtype=np.uint8)
	for j in range(im_hei):
		for i in range(im_wid):
			res_arr[j][i] = new_arr[j][i] * 255


	new_image = Image.fromarray(res_arr)
	new_image.show()
	fullname = "./save/degree/" + filename + "_" + str(c) + "_" + str(f0) + "_" + str(y) + ".bmp"
	new_image.save(fullname, 'BMP')


def greater():
	image, filename = load_image()

	operation = raw_input("Choose operation: linear (l)/ degree (d):")
	if (operation == "l"):
		linear(image, filename)
	elif (operation == "d"):
		degree(image, filename)

def main():
	dec_greater = decorator(greater)
	greater()

def	decorator(func):
	def decorate():
		t1 = time.time()
		func()
		t2 = time.time()
		print ('\n%r %2.2f s' % (func.__name__, (t2 - t1)))
	return decorate

main()
