import numpy as np
from PIL import Image, ImageFilter
import skimage
import skimage.filters
import skimage.exposure
import skimage.morphology

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

def generate_preview(image: Image.Image):
	preview = image.copy()
	bg_black = Image.new("RGB", (350, 350), (0, 0, 0))
	preview.thumbnail((350, 350), Image.LANCZOS)
	# paste in the middle of the black background
	bg_black.paste(preview, ((350 - preview.size[0]) // 2, (350 - preview.size[1]) // 2))
	return bg_black

def color_balance(image: Image.Image, factor: float):
	"""
	Menyesuaikan kecerahan gambar dengan menambahkan nilai tertentu ke setiap piksel.
	"""
	pixels = image.load()
	for x in range(image.size[0]):
		for y in range(image.size[1]):
			# Untuk setiap r g b, tambahkan nilai brightness ke setiap piksel
			# Pastikan tidak ada nilai negatif dan melebihi 255
			pixels[x, y] = tuple([max(0, min(255, int(p * factor))) for p in pixels[x, y]])
	return image

def unsharp_mask(image: Image.Image, factor: float):
	return image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))


def gaussian_blur(image: Image.Image, factor: float):
	"""
	Menyesuaikan kecerahan gambar dengan menambahkan nilai tertentu ke setiap piksel.
	"""
	return image.filter(ImageFilter.GaussianBlur(factor))

def edge_detection(image: Image.Image):
	"""
	Menyesuaikan kecerahan gambar dengan menambahkan nilai tertentu ke setiap piksel.
	"""
	return image.filter(ImageFilter.FIND_EDGES)
