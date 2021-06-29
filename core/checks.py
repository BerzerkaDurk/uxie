import discord
from discord.ext import commands

import config

def is_owner():
    def predicate(ctx):
        return ctx.message.author.id == config.master
    return commands.check(predicate)
