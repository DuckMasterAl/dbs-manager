import discord, json, time
from discord.ext import commands

class Special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx):
        """ Reload the Bot's Commands """
        self.bot.reload_extension('admin')
        self.bot.reload_extension('misc')
        self.bot.reload_extension('moderation')
        self.bot.reload_extension('special')
        await ctx.channel.last_message.add_reaction('\U00002705')
        print(f'--- Bot Shop: Bot Reloaded by {ctx.author} ---')

def setup(bot):
    bot.add_cog(Special(bot))
