import config
import os
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix = config.prefix, owner = config.master)

bot.load_extension(f'core.cog_manager')

bot.run(config.token)