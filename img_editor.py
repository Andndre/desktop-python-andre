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

def squish_image(image: Image.Image, width: int, height: int):
	return image.resize((width, height), Image.LANCZOS)

def blend_images(image1: Image.Image, image2: Image.Image, percentage: int):
	pixels1 = image1.load()
	pixels2 = image2.load()

	# If the size of the images are not the same, raise an error
	if image1.size != image2.size:
		raise ValueError("The images must have the same size")

	# Combine the images
	for x in range(image1.size[0]):
		for y in range(image1.size[1]):
			pixels1[x, y] = tuple([int(p1 * (1 - percentage / 100) + p2 * (percentage / 100)) for p1, p2 in zip(pixels1[x, y], pixels2[x, y])])

	return image1
