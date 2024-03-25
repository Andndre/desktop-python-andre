from PIL import Image
from img_editor import *
from io import BytesIO

def image_disolve(image1: Image.Image, image2: Image.Image, frames: int):
	if image1.size != image2.size:
		image2 = squish_image(image2, image1.size)

	pixels1 = np.array(image1)
	pixels2 = np.array(image2)
	output: list[Image.Image] = []

	print("[Image Disolve]: Generating frames...")
	for i in range(frames + 1):
		pixels = (pixels1 * (1 - i / frames) + pixels2 * (i / frames)).astype(np.uint8)
		output.append(Image.fromarray(pixels))

		print(f"\r[Image Disolve]: Processing frame {i+1}/{frames+1}", end="")
	print()
	print("[Image Disolve]: Completed!")
	return output

def blink_images(image1: Image.Image, image2: Image.Image):
	if image1.size != image2.size:
		image2 = squish_image(image2, image1.size)
	return [image1, image2]

def save_gif(frames: list[Image.Image], filename: str | bytes | BytesIO, fps: int):
	print("[GIF]: Saving GIF...")
	frames[0].save(filename, format="GIF", save_all=True, append_images=frames[1:], loop=0, duration=int(1000/fps))
