import discord

def check_is_image(file: discord.Attachment):
	if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
		return False
	return True
