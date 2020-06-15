import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, user, *, reason='No Reason Provided'):
        """ Kick a member from the server. """
        mod = ctx.author
        reason1 = f'{mod} - {reason}'
        user1 = user
        user2 = user
        if user.__contains__('<') and user.__contains__('>') and user.__contains__('@'): # If User is Mentioned
            user1 = user.replace('<', '')
            user1 = user1.replace('>', '')
            user1 = user1.replace('@', '')
            user1 = user1.replace('!', '')
            user1 = ctx.guild.get_member(int(user1))
        else:
            user1 = discord.utils.get(ctx.guild.members, name=user) # Else Just Search

        if user2 == user and user1 == None: # If search fails, search via userid
            try:
                user1 = ctx.guild.get_member(int(user))
            except:
                pass
        if user1 == None:
            await ctx.send('**:bangbang: ERROR :bangbang:**\nI can\'t find that user!')
            return
        elif user1.id == ctx.guild.owner_id:
            await ctx.send('**:bangbang: ERROR :bangbang:**\nI can\'t kick the owner!')
            return
        member1 = ctx.guild.get_member(user1.id)
        bot1 = ctx.guild.get_member(696425639955136552)
        bot2 = bot1.top_role
        member2 = member1.top_role
        bot = bot2.position
        member = member2.position
        if bot <= member:
            await ctx.send('**:bangbang: ERROR :bangbang:**\nI do not have permission to kick that user!\nTo fix this move my role higher than their role.')
        try:
            await user1.send(f'You just got kicked from **{ctx.guild.name}** by **{mod}** for **{reason}**')
            Fail = False
        except:
            Fail = True
            pass
        if Fail == True:
            rea = ', but no DM was able to be sent.'
        else:
            rea = '.'
        await ctx.guild.kick(user1, reason=reason1)
        await ctx.channel.last_message.delete()
        await ctx.send(f':white_check_mark: {user1.mention} has been kicked for **{reason1}**{rea}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, user, *, reason='No Reason Provided'):
        """ Ban a member from the server. """
        mod = ctx.author
        reason1 = f'{mod} - {reason}'
        user1 = user
        user2 = user
        if user.__contains__('<') and user.__contains__('>') and user.__contains__('@'): # If User is Mentioned
            user1 = user.replace('<', '')
            user1 = user1.replace('>', '')
            user1 = user1.replace('@', '')
            user1 = user1.replace('!', '')
            try:
                user1 = ctx.guild.get_member(int(user1))
            except:
                user1 = None
        else:
            user1 = discord.utils.get(ctx.guild.members, name=user) # Else Just Search

        if user2 == user and user1 == None: # If search fails, search via userid
            try:
                user1 = ctx.guild.get_member(int(user))
            except:
                user1 = None

        if user1 == None:
            await ctx.send('**:bangbang: ERROR :bangbang:**\nI can\'t find that user!')
            return
        elif user1.id == ctx.guild.owner_id:
            await ctx.send('**:bangbang: ERROR :bangbang:**\nI can\'t ban the owner!')
            return
        member1 = ctx.guild.get_member(user1.id)
        bot1 = ctx.guild.get_member(696425639955136552)
        bot2 = bot1.top_role
        member2 = member1.top_role
        bot = bot2.position
        member = member2.position
        if bot <= member:
            await ctx.send(' I do not have permission to ban that user!\nTo fix this move my role higher than their role.')
        try:
            await user1.send(f'You just got banned from **{ctx.guild.name}** by **{mod}** for **{reason}**')
            Fail = False
        except:
            Fail = True
            pass
        if Fail == True:
            rea = ', but no DM was able to be sent.'
        else:
            rea = '.'
        await ctx.guild.ban(user1, reason=reason1)
        await ctx.channel.last_message.delete()
        await ctx.send(f':white_check_mark: {user1.mention} has been banned for **{reason1}**{rea}')

    @commands.command(aliases=['clear', 'massdelete', 'delete', 'del'], usage='[channel] <amount>')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, channel, *, amount=None):
        """ Delete Messages from a Channel. """
        fail = False
        if amount is not None:
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
                return await ctx.send(f'**:bangbang: ERROR :bangbang:**\namount is a required argument that is missing.')
            else:
                amount_to_purge = int(amount) + 1
                await channel1.purge(limit=amount_to_purge)
                if int(amount) == 1:
                    s = ' in'
                else:
                    s = 's in'
                await ctx.send(f':white_check_mark: Purged {amount} message{s} {channel1.mention}!', delete_after=1.5)
        else:
            amount_to_purge = int(channel) + 1
            await ctx.channel.purge(limit=amount_to_purge)
            if int(channel) == 1:
                s = '!'
            else:
                s = 's!'
            await ctx.send(f':white_check_mark: Purged {channel} message{s}', delete_after=1.5)

def setup(bot):
    bot.add_cog(Moderation(bot))
