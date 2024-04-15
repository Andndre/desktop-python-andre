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

# Translates this p5.js code into python
# let img;
# let imgWidth
# let gravity = 2;
# let y;
# let x = 0;
# let goingRight = true;
# let velocity = 1;

# function setup() {
#   createCanvas(400, 400);
#   img = loadImage("images/baboon.png");
#   imgWidth = width / 2;
#   y = imgWidth
# }

# function draw() {
#   background(0, 255, 0);
#   image(img, x, y, imgWidth, imgWidth);
#   if (x + imgWidth >= width) {
#     goingRight = false
#   } else if (x <= 0) {
#     goingRight = true
#   }
#   if (goingRight) {
#     x += 3
#   } else {
#     x -= 3
#   }
#   if (y + imgWidth >= height) {
#     velocity -= 30
#   }
#   y += velocity;
#   velocity += gravity;
# }
def bouncing_image(image: Image.Image):
	width = 400
	img_width = int(width / 2)
	going_right = True
	x = 0
	y = img_width
	gravity = 2
	velocity = 1

	print("[Bouncing Image]: Generating frames...")
	image = squish_image(image, (img_width, img_width))

	frames: list[Image.Image] = []
	bg = Image.new("RGBA", (width, width), (0, 0, 0, 0))

	count = 0

	while True:
		current_frame = bg.copy()
		current_frame.paste(image, (x, y))
		frames.append(current_frame)

		print(f"\r[Bouncing Image]: Processing frame {len(frames)}", end="")

		if x + img_width >= width:
			going_right = False
		elif x < 0:
			if count == 1:
				break
			going_right = True
			count += 1
		if going_right:
			x += 3
		else:
			x -= 3
		if y + img_width >= width:
			velocity -= 30
		y += velocity
		velocity += gravity
	
	print()
	print("[Bouncing Image]: Completed!")

	return frames

def save_gif(frames: list[Image.Image], filename: str | bytes | BytesIO, fps: int):
	print("[GIF]: Saving GIF...")
	frames[0].save(filename, format="GIF", save_all=True, append_images=frames[1:], loop=0, duration=int(1000/fps), disposal=2)
