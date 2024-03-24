from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image, ImageFilter
import discord
import os
import io

from img_editor import *
from helper import *

load_dotenv()

TOKEN = os.getenv('TOKEN')

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.tree.command(name="brighten", description="Brighten an Image")
async def brighten(interaction: discord.Interaction, image: discord.Attachment):
    filename = image.filename

    if not check_is_image(image):
        await interaction.response.send_message("That's not an image!", ephemeral=True)

    image_bytes = io.BytesIO(await image.read())
    img = Image.open(image_bytes)
    img = image_brightness_add(img, 50)

    with io.BytesIO() as output:
        img.save(output, format="PNG")
        output.seek(0)
        await interaction.response.send_message(file=discord.File(fp=output, filename=filename))

@bot.tree.command(name="blur", description="Blur an Image")
async def blur(interaction: discord.Interaction, image: discord.Attachment, blur: int = 5):
    filename = image.filename

    if not check_is_image(image):
        await interaction.response.send_message("That's not an image!", ephemeral=True)
    
    image_bytes = io.BytesIO(await image.read())
    img = Image.open(image_bytes)
    img = img.filter(ImageFilter.GaussianBlur(radius=blur))

    with io.BytesIO() as output:
        img.save(output, format="PNG")
        output.seek(0)
        await interaction.response.send_message(file=discord.File(fp=output, filename=filename))

@bot.tree.command(name="resize", description="Resize an Image")
async def resize(interaction: discord.Interaction, image: discord.Attachment, width: int, height: int):
    filename = image.filename

    if not check_is_image(image):
        await interaction.response.send_message("That's not an image!", ephemeral=True)

    image_bytes = io.BytesIO(await image.read())
    img = Image.open(image_bytes)
    img = squish_image(img, width, height)

    with io.BytesIO() as output:
        img.save(output, format="PNG")
        output.seek(0)
        await interaction.response.send_message(file=discord.File(fp=output, filename=filename))

@bot.tree.command(name="blending", description="Blend two images")
async def blending(interaction: discord.Interaction, image1: discord.Attachment, image2: discord.Attachment, percentage: int = 50):
    filename = image1.filename

    if not check_is_image(image1) or not check_is_image(image2):
        await interaction.response.send_message("That's not an image!", ephemeral=True)
    
    image1_bytes = io.BytesIO(await image1.read())
    image2_bytes = io.BytesIO(await image2.read())

    img1 = Image.open(image1_bytes)
    img2 = Image.open(image2_bytes)

    img = blend_images(img1, img2, percentage)

    with io.BytesIO() as output:
        img.save(output, format="PNG")
        output.seek(0)
        await interaction.response.send_message(file=discord.File(fp=output, filename=filename))

@bot.tree.command(name="giftwo", description="Convert two images into a gif (blink fast!!)")
async def gif(interaction: discord.Interaction, image1: discord.Attachment, image2: discord.Attachment, duration_per_frame: int = 100):
    if not check_is_image(image1) or not check_is_image(image2):
        await interaction.response.send_message("That's not an image!", ephemeral=True)
    
    image1_bytes = io.BytesIO(await image1.read())
    image2_bytes = io.BytesIO(await image2.read())

    await interaction.response.defer()

    img1 = Image.open(image1_bytes)
    img2 = Image.open(image2_bytes)

    # Create GIF
    with io.BytesIO() as output:
        img1.save(output, format="GIF", save_all=True, append_images=[img2], duration=duration_per_frame, loop=0)
        output.seek(0)
        await interaction.followup.send(file=discord.File(fp=output, filename="gif.gif"))

@bot.event
async def on_ready():
    await bot.tree.sync()
    
bot.run(str(TOKEN))
