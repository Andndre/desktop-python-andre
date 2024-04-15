import numpy as np
from PIL import Image

def image_brightness_add(image: Image.Image, brightness: int):
	"""
	Menyesuaikan kecerahan gambar dengan menambahkan nilai tertentu ke setiap piksel.
	"""
	pixels = image.load()
	for x in range(image.size[0]):
		for y in range(image.size[1]):
			# Untuk setiap r g b, tambahkan nilai brightness ke setiap piksel
			# Pastikan tidak ada nilai negatif dan melebihi 255
			pixels[x, y] = tuple([max(0, min(255, p + brightness)) for p in pixels[x, y]])
	return image

def squish_image(image: Image.Image, size: tuple[int, int]):
	width, height = size
	return image.resize((width, height), Image.LANCZOS)	

def blend_images(image1: Image.Image, image2: Image.Image, percentage: int):

	# If the size of the images are not the same, raise an error
	if image1.size != image2.size:
		image2 = squish_image(image2, image1.size)

	pixels1 = np.array(image1)
	pixels2 = np.array(image2)
	
	# Combine the images
	pixels1 = (pixels1 * (1 - percentage / 100) + pixels2 * (percentage / 100)).astype(np.uint8)

	return Image.fromarray(pixels1)
