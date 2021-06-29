import dload
import config
import discord

from discord.ext import commands
from core import checks

class RefreshMaster(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def refreshmaster(self, ctx):
        dload.save('https://raw.githubusercontent.com/PokeMiners/game_masters/master/latest/latest.json',
                   'data/latest.json', True)
        
        await ctx.send('Latest game master imported successfully from PokeMiners.')

def setup(bot):
    bot.add_cog(RefreshMaster(bot))
