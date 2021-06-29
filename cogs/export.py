import discord
from discord.ext import commands

from core import checks

class Export(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def export(self, ctx, arg = ''):
        if arg not in ['pokemon', 'forms']:
            await ctx.send(f'Argument \'{arg}\' is not valid for command export.')
            return
        if arg == 'pokemon':
            file = discord.File('data/masterdata.csv', filename = 'masterdata.csv')
            await ctx.send('Here is your file.', file = file)
        if arg == 'forms':
            file = discord.File('data/forms.json', filename= 'forms.json')
            await ctx.send('Here ya go...', file= file)

def setup(bot):
    bot.add_cog(Export(bot))
