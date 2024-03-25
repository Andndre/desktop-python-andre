import discord
import io
from PIL import Image
from animate_image import *

def check_is_image(file: discord.Attachment):
	if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
		return False
	return True

async def get_pillow_image(file: discord.Attachment):
	return Image.open(io.BytesIO(await file.read()))

async def send_image(interaction: discord.Interaction[discord.Client], img: Image.Image, filename: str, format: str = "PNG"):
	with io.BytesIO() as output:
		img.save(output, format=format)
		output.seek(0)
		await interaction.followup.send(file=discord.File(fp=output, filename=filename))

async def send_gif(interaction: discord.Interaction[discord.Client], frames: list[Image.Image], filename: str, fps: int):
    with io.BytesIO() as output:
        save_gif(frames, output, fps)
        output.seek(0)
        await interaction.followup.send(file=discord.File(fp=output, filename=filename))
