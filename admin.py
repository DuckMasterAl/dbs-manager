import discord, json
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage='[channel] <message>')
    @commands.is_owner()# Delete this if you want anyone to be able to use the "say" command
    async def say(self, ctx, channel, message=None):
        """ Make's the Bot Say a Message! """
        fail = False
        channel1 = channel
        if channel.__contains__('<') and channel.__contains__('>') and channel.__contains__('#'):
            channel1 = channel.replace('<', '')
            channel1 = channel1.replace('>', '')
            channel1 = channel1.replace('#', '')
            try:
                channel1 = ctx.guild.get_channel(int(channel1))
            except:
                fail = True
        else:
            try:
                channel1 = ctx.guild.get_channel(int(channel1))
            except:
                fail = True
        if fail == True:
            await ctx.channel.last_message.delete()
            return await ctx.send(channel)
        else:
            if message is None:
                return await ctx.send(f'**:bangbang: ERROR :bangbang:**\nmessage is a required argument that is missing.')
            await channel1.send(message)
            await ctx.channel.last_message.add_reaction('\U00002705')

    @commands.command()
    async def reload(self, ctx):
        self.bot.reload_extension('admin')
        await ctx.channel.last_message.add_reaction('\U00002705')
        print('---- -- ---- -- -- --')

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """ Shutdown the Bot. """
        await ctx.send('Ok, Shutting down now. Bye!')
        await self.bot.change_presence(activity=discord.Game(type=0, name='Shutting Down'), status=discord.Status.dnd)
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user, *, message):
        """ Makes the Bot DM Someone. """
        user1 = user
        if user.__contains__('<') and user.__contains__('>') and user.__contains__('@'):
            user1 = user.replace('<', '')
            user1 = user1.replace('>', '')
            user1 = user1.replace('@', '')
            user1 = user1.replace('!', '')
            user1 = self.bot.get_user(int(user1))
        else:
            try:
                user1 = self.bot.get_user(int(user))
            except:
                pass

        if user1 is None:
            return await ctx.send(f'**:bangbang: ERROR :bangbang:**\nI cannot find that user!')
        try:
            await user1.send(message)
            await ctx.send(f"<:fancycheck:681610286444314668> Sent a DM to **{user1}**")
        except discord.Forbidden:
            await ctx.send('**:bangbang: ERROR :bangbang:**\nI am unable to DM that user.')

def setup(bot):
    bot.add_cog(Admin(bot))
