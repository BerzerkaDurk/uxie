import discord
from discord.ext import commands

from core import pokemon
from core import checks

class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def test(self, ctx):

        poke = pokemon.Pokemon

        poke.species = 'bulbasaur'
        await ctx.send(poke.species)

def setup(bot):
    bot.add_cog(Test(bot))
