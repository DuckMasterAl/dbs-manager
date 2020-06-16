import discord, json, time
from discord.ext import commands

class Special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Special(bot))
