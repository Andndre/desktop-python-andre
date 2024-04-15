from discord.ext import commands
from dotenv import load_dotenv
from PIL import ImageFilter
import discord
import os

from img_editor import *
from helper import *
from animate_image import *

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
@discord.app_commands.describe(image="The image")
async def brighten(interaction: discord.Interaction, image: discord.Attachment):
    await interaction.response.defer()
    filename = image.filename
    if not check_is_image(image):
        await interaction.followup.send("That's not an image!", ephemeral=True)
        return
    img = await get_pillow_image(image)
    img = image_brightness_add(img, 50)
    await send_image(interaction, img, filename)

@bot.tree.command(name="blur", description="Blur an Image")
@discord.app_commands.describe(image="The image", blur="Blur")
async def blur(interaction: discord.Interaction, image: discord.Attachment, blur: int):
    await interaction.response.defer()
    filename = image.filename
    if not check_is_image(image):
        await interaction.followup.send("That's not an image!", ephemeral=True)
        return
    img = await get_pillow_image(image)
    img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    await send_image(interaction, img, filename)

@bot.tree.command(name="resize", description="Resize an Image")
@discord.app_commands.describe(image="The image", width="Width", height="Height")
async def resize(interaction: discord.Interaction, image: discord.Attachment, width: int, height: int):
    await interaction.response.defer()
    filename = image.filename
    if not check_is_image(image):
        await interaction.followup.send("That's not an image!", ephemeral=True)
        return
    img = await get_pillow_image(image)
    img = squish_image(img, (width, height))
    await send_image(interaction, img, filename)

@bot.tree.command(name="blending", description="Blend two images")
@discord.app_commands.describe(image1="The first image", image2="The second image", percentage="Percentage")
async def blending(interaction: discord.Interaction, image1: discord.Attachment, image2: discord.Attachment, percentage: discord.app_commands.Range[int, 0, 100]):
    await interaction.response.defer()
    filename = image1.filename
    if not check_is_image(image1) or not check_is_image(image2):
        await interaction.followup.send("That's not an image!", ephemeral=True)
        return
    if percentage < 0 or percentage > 100:
        await interaction.followup.send("Percentage must be between 0 and 100!", ephemeral=True)
        return
    
    img1 = await get_pillow_image(image1)
    img2 = await get_pillow_image(image2)
    img = blend_images(img1, img2, percentage)
    await send_image(interaction, img, filename)

@bot.tree.command(name="gifblink", description="Convert two images into a gif (blink fast!!)")
@discord.app_commands.describe(image1="The first image", image2="The second image", duration_per_frame="Duration per frame in milliseconds")
async def gifblink(interaction: discord.Interaction, image1: discord.Attachment, image2: discord.Attachment, duration_per_frame: discord.app_commands.Range[int, 1, 500]):
    await interaction.response.defer()

    if not check_is_image(image1) or not check_is_image(image2):
        await interaction.followup.send("That's not an image!", ephemeral=True)
        return
    
    if duration_per_frame <= 0:
        await interaction.followup.send("Duration must be greater than 0!", ephemeral=True)

    img1 = await get_pillow_image(image1)
    img2 = await get_pillow_image(image2)

    result = blink_images(img1, img2)

    await send_gif(interaction, result, "gif.gif", int(1000/duration_per_frame))

@bot.tree.command(name="gifdisolve", description="Disolve two images (gif)")
@discord.app_commands.describe(image1="The first image", image2="The second image", duration="Duration in seconds")
async def gifdisolve(interaction: discord.Interaction, image1: discord.Attachment, image2: discord.Attachment, duration: int = 3):
    await interaction.response.defer()

    if not check_is_image(image1) or not check_is_image(image2):
        await interaction.followup.send("That's not an image!", ephemeral=True)
        return

    if duration <= 0:
        await interaction.followup.send("Duration must be greater than 0!", ephemeral=True)
        return

    img1 = await get_pillow_image(image1)
    img2 = await get_pillow_image(image2)

    frames = image_disolve(img1, img2, int(15*duration))

    await send_gif(interaction, frames, "gif.gif", 15)

@bot.tree.command(name="gifbouncing", description="Bouncing image (gif)")
@discord.app_commands.describe(image="The image")
async def gifbouncing(interaction: discord.Interaction, image: discord.Attachment):
    await interaction.response.defer()

    if not check_is_image(image):
        await interaction.followup.send("That's not an image!", ephemeral=True)
        return

    img = await get_pillow_image(image)

    frames = bouncing_image(img)

    await send_gif(interaction, frames, "gif.gif", 15)


@bot.event
async def on_ready():
    await bot.tree.sync()
    
bot.run(str(TOKEN))
