from discord.ext.commands.bot import Bot
import config
import os
import discord
from discord.ext import commands

class CogManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Module --{extension}-- loaded')
        
    @commands.command()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Module --{extension}-- unloaded')

    @commands.command()
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Module --{extension.upper()}-- reloaded successfully.')

def setup(bot):
    bot.add_cog(CogManager(bot))

    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            filename = filename[:-3]
            bot.load_extension(f'cogs.{filename}')
            print(f'Module --{filename.upper()}-- loaded successfully.')
