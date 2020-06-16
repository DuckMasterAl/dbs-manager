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

    @commands.command()
    async def new(self, ctx, *, subject=None):
        """ Create a Ticket!
        Ticket Categories are Report, Question, and Other. """
        ticket_blacklist = open('/root/Bot_Shop/ticket_blacklist.txt', 'r').read()
        ticket_blacklist = ticket_blacklist.split('\n')
        if str(ctx.author.id) in ticket_blacklist:
            await ctx.send(f':x: You are Blacklisted from Making Tickets!')
            return
        guild = self.bot.get_guild(717112726408921218)
        await ctx.channel.last_message.delete()
        duckville_helper = guild.get_role(717112726412984398)
        member1 = guild.get_member(ctx.author.id)
        category = self.bot.get_channel(722291995699052584)
        if subject == None:
            def check_msg(m):
                if ctx.author == m.author and ctx.channel == m.channel:
                    return True
                else:
                    return False
            m1 = await ctx.send('What\'s the Subject of your Support Ticket?')
            try:
                msg = await self.bot.wait_for('message', check=check_msg, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send(':x: You took too long to answer the question!')
                return
            subject = msg.content
            await m1.delete()
            await msg.delete()
            if subject.lower() == 'cancel':
                await ctx.send(':x: Canceled Creating the Support Ticket.')
                return
        react_msg = await ctx.send(f'**Identify Your Ticket\'s Topic:**\n:bangbang: - Report\n:grey_question: - Server Question\n:robot: - Buy a Bot\n:x: - Cancel Your Ticket Creation')
        bangbang = '\U0000203c'
        news = '\U0001f916'
        question = '\U00002754'
        cancel_emoji = '\U0000274c'
        await react_msg.add_reaction(bangbang)
        await react_msg.add_reaction(question)
        await react_msg.add_reaction(news)
        await react_msg.add_reaction(cancel_emoji)
        def check_react(reaction, user_react):
            if ctx.author == user_react:
                if reaction.emoji == bangbang or reaction.emoji == question or reaction.emoji == news or reaction.emoji == cancel_emoji:
                    return True
                else:
                    return False
            else:
                return False
        try:
            reaction, user_react = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_react)
        except asyncio.TimeoutError:
            await ctx.send(':x: You took too long to react to the message!')
            return
        else:
            if reaction.emoji == bangbang:
                m = []
                online = discord.Status.online
                for member in duckville_helper.members:
                    if member.is_on_mobile():
                        return
                    if member.status == online:
                        m.append(f'{member.mention}')
                content = ' '.join(m)
                content = f'{content} {ctx.author.mention}'
                ticket_prefix = 'report'
                topic = 'Report'
            elif reaction.emoji == question:
                content = ctx.author.mention
                ticket_prefix = 'question'
                topic = 'Question'
            elif reaction.emoji == news:
                content = ctx.author.mention
                ticket_prefix = 'buy-bot'
                topic = 'Buy a Bot'
            elif reaction.emoji == cancel_emoji:
                await ctx.send(f':white_check_mark: Canceled the Ticket Making Process.', delete_after=10)
                return await react_msg.delete()
            await react_msg.delete()
        channel = await guild.create_text_channel(f'{ticket_prefix}-{member1.display_name}', category=category, reason=f'{ctx.author} - Ticket Creation', topic=f'USERID: {ctx.author.id}')
        await channel.set_permissions(guild.default_role, read_messages=False, reason=f'{ctx.author} - Ticket Creation')
        await channel.set_permissions(ctx.author, read_messages=True, send_messages=True, manage_messages=False, reason=f'{ctx.author} - Ticket Creation')
        await channel.set_permissions(duckville_helper, read_messages=True, send_messages=True, reason=f'{ctx.author} - Ticket Creation')#, manage_channel=True)
        embed = discord.Embed(title='Duckville Support', colour=discord.Colour(7506394), description=f'Hey {ctx.author.mention}! Thanks for making a support ticket.\nA duckville helper will respond to you as soon as possible.\nTopic: **{topic}**\nSubject: **{subject}**')
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await channel.send(embed=embed)
        delcontent = await channel.send(f'{content}', delete_after=0.01)
        await ctx.send(f':white_check_mark: Created your Support Ticket --> {channel.mention}', delete_after=10)

    @commands.command()
    @commands.guild_only()
    async def close(self, ctx, *, reason=None):
        """ Close a Ticket """
        if ctx.channel.category_id != 722291995699052584:
            await ctx.send(f':x: You can only do this command in a Support Ticket.')
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        archive = ctx.guild.get_channel(711227298157953035)
        tuser = self.bot.get_user(int(ticket_owner))
        dvhelper = ctx.guild.get_role(519482266473332736)
        member = ctx.guild.get_member(ctx.author.id)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = True
        await ctx.channel.last_message.delete()
        if reason == None:
            def check_msg(m):
                if ctx.author == m.author and ctx.channel == m.channel:
                    return True
                else:
                    return False
            m1 = await ctx.send('What\'s the reason for closing the ticket?')
            try:
                m2 = await self.bot.wait_for('message', check=check_msg, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send(':x: You took too long to answer the question!')
                return
            reason = m2.content
            await m1.delete()
            await m2.delete()
            if reason.lower() == 'cancel':
                await ctx.send(':x: Canceled Closing the Support Ticket.')
                return
        if dvhelper in member.roles or ticket_owner == str(ctx.author.id):
            msg = await ctx.send(f':yellow_circle: Sending the Message and Updating Permissions...')
            try:
                await tuser.send(f'Your ticket has been closed by **{member.display_name}** with reason **{reason}**\nYou can read the chat history here: {msg.jump_url}')
            except:
                await ctx.send(f'{tuser.mention} your ticket has been closed by {member.display_name} with reason {reason}', delete_after=5)
            await ctx.channel.edit(category=archive, reason=f'{ctx.author} - Ticket Close Command', sync_permissions=True, position=0)
            await ctx.channel.set_permissions(tuser, overwrite=overwrite)
            await msg.edit(content=f':lock: Ticket Closed by **{member.display_name}**\nReason: **{reason}**')
        else:
            await ctx.send(':x: You don\'t have permission to do this command.')

    @commands.command()
    @commands.guild_only()
    async def add(self, ctx, *, user):
        """ Add Someone to a Ticket """
        if ctx.channel.category_id != 722291995699052584:
            await ctx.send(f':x: You can only do this command in a Support Ticket.')
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
        dvhelper = ctx.guild.get_role(519482266473332736)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        if dvhelper in ctx_member.roles or ticket_owner == str(ctx.author.id):
            user = user.lower()
            user1 = None
            embed_user = ctx.author
            u = []
            m = []
            failn = []
            faily = []
            def check(m):
                if ctx.author == m.author and ctx.channel == m.channel:
                    try:
                        m1 = int(m.content)
                    except:
                        faily.append('n')
                        return True
                    message_0 = m1 - 1
                    if message_0 >= users_len or m1 <= 0:
                        faily.append('n')
                        return True
                    else:
                        failn.append('n')
                        return True
                else:
                    faily.append('n')
                    return False
            guildmem = ctx.guild.members
            for member in guildmem:
                name = f'{member.name}#{member.discriminator}'
                name = name.lower()
                dname = member.display_name
                dname = dname.lower()
                oname = member.name
                oname = oname.lower()
                if dname.__contains__(f'{user}') or name == (f'{user}') or oname.__contains__(f'{user}'):
                    u.append(f'{member.mention}')
                    m.append(f'{member.id}')
            if len(u) == 1:# If it returns only 1 member
                pop = m.pop(0)
                user1 = ctx.guild.get_member(int(pop))
            elif len(u) == 0:# If it returns 0 members
                if user.startswith('<@') and user.endswith('>'):
                    user1 = user.replace('<', '')
                    user1 = user1.replace('>', '')
                    user1 = user1.replace('!', '')
                    user1 = user1.replace('@', '')
                    user1 = ctx.guild.get_member(int(user1))
                else:
                    try:
                        user1 = ctx.guild.get_member(int(user))
                    except:
                        user1 = None
                        pass
                if user1 == None:
                    embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='I can not find that user!')
                    embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                    embed.set_footer(text='If you need help please do the -support command.')
                    await ctx.send(embed=embed)
                    return
            elif len(u) >= 10:
                embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='Too many users found. Please be more specific.')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                embed.set_footer(text='If you need help please do the -support command.')
                await ctx.send(embed=embed)
                return
            else:# If it returns more than 1 member
                a = ['1']
                users_list = []
                for item in u:
                    num = len(a)
                    a.append('f')
                    users_list.append(f'{num}. {item}')
                users_len = len(users_list)
                users_list = '\n'.join(users_list)# -- -- -- ADD RESULT TEXT BELOW -- -- --
                embed = discord.Embed(title='Multiple Members Found!', colour=discord.Colour(7506394), description=f'Please type the number that corresponds to the member you want to add to the ticket.\n{users_list}')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                msg2 = await ctx.send(embed=embed)
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    await ctx.send(':x: You took too long to answer the question!')
                    return
                if len(failn) >= 1:
                    msg1 = int(msg.content)
                    popnum = msg1 - 1
                    user2 = m.pop(popnum)
                    user1 = ctx.guild.get_member(int(user2))
                elif len(faily) >= 1:
                    await ctx.send(f':x: Invalid Number.')
                    return
            if discord.PermissionOverwrite.is_empty(ctx.channel.overwrites_for(user1)) == False:
                await ctx.send(':x: You can\'t add someone to the ticket if they\'ve already been added!')
                return
            try:
                await user1.send(f':inbox_tray: You\'ve been added to **{ctx.channel.mention}** by **{ctx.author.display_name}.**')
            except:
                pass
            await ctx.channel.set_permissions(user1, read_messages=True)
            await starting_msg.delete()
            try:
                await msg2.delete()
                await msg.delete()
            except:
                pass
            await ctx.send(f':white_check_mark: **{ctx_member.display_name}** added **{user1.display_name}** to the channel.')
        else:
            await ctx.send(':x: You don\'t have permission to do this command.')

    @commands.command()
    @commands.guild_only()
    async def remove(self, ctx, *, user):
        """ Remove Someone from a Ticket """
        if ctx.channel.category_id != 722291995699052584:
            await ctx.send(f':x: You can only do this command in a Support Ticket.')
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
        tmember = ctx.guild.get_member(int(ticket_owner))
        dvhelper = ctx.guild.get_role(519482266473332736)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        if dvhelper in ctx_member.roles or ticket_owner == str(ctx.author.id):
            user = user.lower()
            user1 = None
            embed_user = ctx.author
            u = []
            m = []
            failn = []
            faily = []
            def check(m):
                if ctx.author == m.author and ctx.channel == m.channel:
                    try:
                        m1 = int(m.content)
                    except:
                        faily.append('n')
                        return True
                    message_0 = m1 - 1
                    if message_0 >= users_len or m1 <= 0:
                        faily.append('n')
                        return True
                    else:
                        failn.append('n')
                        return True
                else:
                    faily.append('n')
                    return False
            guildmem = ctx.guild.members
            for member in guildmem:
                name = f'{member.name}#{member.discriminator}'
                name = name.lower()
                dname = member.display_name
                dname = dname.lower()
                oname = member.name
                oname = oname.lower()
                if dname.__contains__(f'{user}') or name == (f'{user}') or oname.__contains__(f'{user}'):
                    u.append(f'{member.mention}')
                    m.append(f'{member.id}')
            if len(u) == 1:# If it returns only 1 member
                pop = m.pop(0)
                user1 = ctx.guild.get_member(int(pop))
            elif len(u) == 0:# If it returns 0 members
                if user.startswith('<@') and user.endswith('>'):
                    user1 = user.replace('<', '')
                    user1 = user1.replace('>', '')
                    user1 = user1.replace('!', '')
                    user1 = user1.replace('@', '')
                    user1 = ctx.guild.get_member(int(user1))
                else:
                    try:
                        user1 = ctx.guild.get_member(int(user))
                    except:
                        user1 = None
                        pass
                if user1 == None:
                    embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='I can not find that user!')
                    embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                    embed.set_footer(text='If you need help please do the -support command.')
                    await ctx.send(embed=embed)
                    return
            elif len(u) >= 10:
                embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='Too many users found. Please be more specific.')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                embed.set_footer(text='If you need help please do the -support command.')
                await ctx.send(embed=embed)
                return
            else:# If it returns more than 1 member
                a = ['1']
                users_list = []
                for item in u:
                    num = len(a)
                    a.append('f')
                    users_list.append(f'{num}. {item}')
                users_len = len(users_list)
                users_list = '\n'.join(users_list)# -- -- -- ADD RESULT TEXT BELOW -- -- --
                embed = discord.Embed(title='Multiple Members Found!', colour=discord.Colour(7506394), description=f'Please type the number that corresponds to the member you want to remove from the ticket.\n{users_list}')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                msg2 = await ctx.send(embed=embed)
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    await ctx.send(':x: You took too long to answer the question!')
                    return
                if len(failn) >= 1:
                    msg1 = int(msg.content)
                    popnum = msg1 - 1
                    user2 = m.pop(popnum)
                    user1 = ctx.guild.get_member(int(user2))
                elif len(faily) >= 1:
                    await ctx.send(f':x: Invalid Number.')
                    return
            if user1 == tmember:
                await ctx.send(f':x: You can\'t remove the Ticket Owner from the ticket!')
                return
            elif dvhelper in user1.roles:
                await ctx.send(f':x: You cannot remove a Duckville Helper from the Ticket!')
                return
            elif user1.id == 235148962103951360 or user1.id == 681598966399369341 or user1.id == 534589798267224065 or user1.id == 356950275044671499:
                await ctx.send(f':x: You cannot remove this bot. It has permission to see every channel.')
                return
            elif discord.PermissionOverwrite.is_empty(ctx.channel.overwrites_for(user1)):
                await ctx.send(f':x: {user1.display_name} hasn\'t been added to the Ticket!')
                return
            await ctx.channel.set_permissions(user1, overwrite=None)
            await starting_msg.delete()
            try:
                await msg2.delete()
                await msg.delete()
            except:
                pass
            await ctx.send(f':white_check_mark: **{ctx_member.display_name}** removed **{user1.display_name}** from the channel.')
        else:
            await ctx.send(':x: You don\'t have permission to do this command.')

    @commands.command()
    @commands.guild_only()
    async def rename(self, ctx, *, prefix):
        """ Rename a Ticket's Prefix """
        if ctx.channel.category_id != 722291995699052584:
            await ctx.send(f':x: You can only do this command in a Support Ticket.')
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
        tmember = ctx.guild.get_member(int(ticket_owner))
        dvhelper = ctx.guild.get_role(519482266473332736)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        if dvhelper in ctx_member.roles:
            await ctx.channel.edit(name=f'{prefix}-{tmember.display_name}')
            await ctx.send(f':white_check_mark: **{ctx_member.display_name}** renamed the channel to **{ctx.channel.name}**')
            await starting_msg.delete()
        else:
            await ctx.send(':x: You don\'t have permission to do this command.')

    @commands.command(aliases=['transferowner', 'ownertransfer'])
    @commands.guild_only()
    async def transfer(self, ctx, *, user):
        """ Make Someone Else the Ticket Owner of a Ticket """
        ticket_blacklist = open('/root/Bot_Shop/ticket_blacklist.txt', 'r').read()
        ticket_blacklist = ticket_blacklist.split('\n')
        if ctx.channel.category_id != 722291995699052584:
            await ctx.send(f':x: You can only do this command in a Support Ticket.')
            return
        ticket_owner = ctx.channel.topic
        ticket_owner = ticket_owner.replace('USERID: ', '')
        tuser = self.bot.get_user(int(ticket_owner))
        tmember = ctx.guild.get_member(int(ticket_owner))
        dvhelper = ctx.guild.get_role(519482266473332736)
        ctx_member = ctx.guild.get_member(ctx.author.id)
        starting_msg = ctx.channel.last_message
        if dvhelper in ctx_member.roles or ticket_owner == str(ctx.author.id):
            user = user.lower()
            user1 = None
            embed_user = ctx.author
            u = []
            m = []
            failn = []
            faily = []
            def check(m):
                if ctx.author == m.author and ctx.channel == m.channel:
                    try:
                        m1 = int(m.content)
                    except:
                        faily.append('n')
                        return True
                    message_0 = m1 - 1
                    if message_0 >= users_len or m1 <= 0:
                        faily.append('n')
                        return True
                    else:
                        failn.append('n')
                        return True
                else:
                    faily.append('n')
                    return False
            guildmem = ctx.guild.members
            for member in guildmem:
                name = f'{member.name}#{member.discriminator}'
                name = name.lower()
                dname = member.display_name
                dname = dname.lower()
                oname = member.name
                oname = oname.lower()
                if dname.__contains__(f'{user}') or name == (f'{user}') or oname.__contains__(f'{user}'):
                    u.append(f'{member.mention}')
                    m.append(f'{member.id}')
            if len(u) == 1:# If it returns only 1 member
                pop = m.pop(0)
                user1 = ctx.guild.get_member(int(pop))
            elif len(u) == 0:# If it returns 0 members
                if user.startswith('<@') and user.endswith('>'):
                    user1 = user.replace('<', '')
                    user1 = user1.replace('>', '')
                    user1 = user1.replace('!', '')
                    user1 = user1.replace('@', '')
                    user1 = ctx.guild.get_member(int(user1))
                else:
                    try:
                        user1 = ctx.guild.get_member(int(user))
                    except:
                        user1 = None
                        pass
                if user1 == None:
                    embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='I can not find that user!')
                    embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                    embed.set_footer(text='If you need help please do the -support command.')
                    await ctx.send(embed=embed)
                    return
            elif len(u) >= 10:
                embed = discord.Embed(title='OOPS! An error has occured >.<', colour=discord.Colour(0xff0000), description='Too many users found. Please be more specific.')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/678014140203401246.png?v=1")
                embed.set_footer(text='If you need help please do the -support command.')
                await ctx.send(embed=embed)
                return
            else:# If it returns more than 1 member
                a = ['1']
                users_list = []
                for item in u:
                    num = len(a)
                    a.append('f')
                    users_list.append(f'{num}. {item}')
                users_len = len(users_list)
                users_list = '\n'.join(users_list)# -- -- -- ADD RESULT TEXT BELOW -- -- --
                embed = discord.Embed(title='Multiple Members Found!', colour=discord.Colour(7506394), description=f'Please type the number that corresponds to the member you want to make the ticket owner.\n{users_list}')
                embed.set_author(name=f'{embed_user}', icon_url=f'{embed_user.avatar_url}')
                msg2 = await ctx.send(embed=embed)
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    await ctx.send(':x: You took too long to answer the question!')
                    return
                if len(failn) >= 1:
                    msg1 = int(msg.content)
                    popnum = msg1 - 1
                    user2 = m.pop(popnum)
                    user1 = ctx.guild.get_member(int(user2))
                elif len(faily) >= 1:
                    await ctx.send(f':x: Invalid Number.')
                    return
            if user1.bot == True:
                await ctx.send(f':x: You cannot transfer a Ticket to a Bot!')
                return
            elif user1.id == tuser.id:
                await ctx.send(f':x: That Person is already the Ticket Owner!')
                return
            elif str(user1.id) in ticket_blacklist and dvhelper not in ctx_member.roles:
                await ctx.send(f':x: You cannot Transfer Ticket Ownership to a Blacklisted User!')
                return
            elif str(user1.id) in ticket_blacklist and dvhelper in ctx_member.roles:
                def check_react(reaction, user_react):
                    if ctx.author == user_react:
                        if reaction.emoji == '\U00002705' or reaction.emoji == '\U0000274c':
                            return True
                        else:
                            return False
                    else:
                        return False
                confirm_msg = await ctx.send(f':warning: You are making a Blacklisted User the Ticket Owner.\nAre you sure you want to continue?')
                await confirm_msg.add_reaction('\U00002705')
                await confirm_msg.add_reaction('\U0000274c')
                try:
                    reaction, user_react = await self.bot.wait_for('reaction_add', timeout=120.0, check=check_react)
                except asyncio.TimeoutError:
                    await ctx.author.send(':x: You took too long to react to the message!')
                    return
                else:
                    if reaction.emoji == check:
                        await confirm_msg.delete()
                    elif reaction.emoji == redx:
                        await ctx.send(':white_check_mark: Not adding them to the Ticket.', delete_after=5)
                        await confirm_msg.delete()
                        await starting_msg.delete()
                        try:
                            await msg2.delete()
                            await msg.delete()
                        except:
                            pass
                        return
            await ctx.channel.set_permissions(user1, read_messages=True, send_messages=True, manage_messages=False, reason=f'{ctx.author} - Transferring Ticket Ownership')
            await ctx.channel.set_permissions(tmember, read_messages=True, send_messages=None, manage_messages=None, reason=f'{ctx.author} - Transferring Ticket Ownership')
            if tuser.id != ctx.author.id:
                await tuser.send(f'Your Ticket ({ctx.channel.mention}) was transferred to **{user1.display_name}**')
            elif user1.id != ctx.author.id:
                await user1.send(f'You\'ve are now the owner of {ctx.channel.mention}.')
            await ctx.channel.edit(topic=f'USERID: {user1.id}', name=f'ticket-{user1.display_name}', reason=f'{ctx.author} - Transferring Ticket Ownership')
            await ctx.send(f':white_check_mark: **{ctx_member.display_name}** Transferred Ticket Ownership from {tmember.display_name} to **{user1.display_name}**')
            await starting_msg.delete()
            try:
                await msg2.delete()
                await msg.delete()
            except:
                pass
        else:
            await ctx.send(':x: You don\'t have permission to do this command.')

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        """ Make a suggestion. """
        guild = self.bot.get_guild(717112726408921218)
        channel = guild.get_channel(717112726538944515)
        user = ctx.author
        userid = ctx.author.id
        embed = discord.Embed(title=f'Suggestion from {user}', colour=discord.Colour(7506394), description=f'{suggestion}')
        embed.set_author(name=f'{user}', icon_url=f'{user.avatar_url}')
        embed.set_footer(text=f'User ID: {user.id}')
        message = await channel.send(embed=embed)
        await message.add_reaction('\U00002705')
        await message.add_reaction('\U0000274c')
        await ctx.send(f':white_check_mark: Posted your suggestion in {channel.mention}!')

    @commands.command()
    @commands.has_role(717112726412984398)
    async def deny(self, ctx, message_id, *, reason):
        """ Deny a suggestion. """
        message_id = int(message_id)
        guild = self.bot.get_guild(717112726408921218)
        channel = guild.get_channel(717112726538944515)
        try:
            message = await channel.fetch_message(message_id)
        except:
            await ctx.send(f':x: I cannot find that suggestion.')
            return
        content = message.embeds
        for embed in content:
            user = ctx.author
            footer = embed.footer
            footer = str(footer)
            footer = footer.replace("EmbedProxy(text='User ID: ", '')
            footer = footer.replace("')", '')
            name = self.bot.get_user(int(footer))
            embed = discord.Embed(title=f'Suggestion Denied by {user}', colour=discord.Colour(12255253), description=f'{embed.description}')
            embed.set_author(name=f'{name}', icon_url=f'{name.avatar_url}')
            embed.add_field(name=f'Reason from {user.name}:', value=f'{reason}')
            embed.set_footer(text=f'User ID: {name.id}')
        try:
            await message.edit(embed=embed)
        except:
            await ctx.send(f':x: I cannot find that suggestion.')
            return
        await ctx.send(f':white_check_mark: Denied the suggestion {message_id}.')
        name_embed = discord.Embed(title=f'Suggestion Denied by {user}', colour=discord.Colour(12255253), description=f'{embed.description}')
        name_embed.set_author(name=f'{name}', icon_url=f'{name.avatar_url}')
        name_embed.add_field(name=f'Reason from {user.name}:', value=f'{reason}')
        await name.send(f'Hey {name.mention}, {user} just denied your suggestion.', embed=name_embed)
        try:
            await message.clear_reactions()
        except:
            pass

    @commands.command()
    @commands.has_role(717112726412984398)
    async def approve(self, ctx, message_id, *, reason):
        """ Approve a suggestion. """
        message_id = int(message_id)
        guild = self.bot.get_guild(717112726408921218)
        channel = guild.get_channel(717112726538944515)
        try:
            message = await channel.fetch_message(message_id)
        except:
            await ctx.send(f':x: I cannot find that suggestion.')
            return
        content = message.embeds
        for embed in content:
            user = ctx.author
            footer = embed.footer
            footer = str(footer)
            footer = footer.replace("EmbedProxy(text='User ID: ", '')
            footer = footer.replace("')", '')
            name = self.bot.get_user(int(footer))
            embed = discord.Embed(title=f'Suggestion Approved by {user}', colour=discord.Colour(6203913), description=f'{embed.description}')
            embed.set_author(name=f'{name}', icon_url=f'{name.avatar_url}')
            embed.add_field(name=f'Reason from {user.name}:', value=f'{reason}')
            embed.set_footer(text=f'User ID: {name.id}')
        try:
            await message.edit(embed=embed)
        except:
            await ctx.send(f':x: I cannot find that suggestion.')
            return
        await ctx.send(f':white_check_mark: Approved the suggestion {message_id}.')
        name_embed = discord.Embed(title=f'Suggestion Approved by {user}', colour=discord.Colour(6203913), description=f'{embed.description}')
        name_embed.set_author(name=f'{name}', icon_url=f'{name.avatar_url}')
        name_embed.add_field(name=f'Reason from {user.name}:', value=f'{reason}')
        await name.send(f'Hey {name.mention}, {user} just approved your suggestion.', embed=name_embed)
        try:
            await message.clear_reactions()
        except:
            pass

    @commands.command(aliases=['implement', 'done'])
    @commands.has_role(717112726412984398)
    async def implemented(self, ctx, message_id, *, reason):
        """ Mark a suggestion as implemented. """
        message_id = int(message_id)
        guild = self.bot.get_guild(717112726408921218)
        channel = guild.get_channel(717112726538944515)
        try:
            message = await channel.fetch_message(message_id)
        except:
            await ctx.send(f':x: I cannot find that suggestion.')
            return
        content = message.embeds
        for embed in content:
            user = ctx.author
            footer = embed.footer
            footer = str(footer)
            footer = footer.replace("EmbedProxy(text='User ID: ", '')
            footer = footer.replace("')", '')
            name = self.bot.get_user(int(footer))
        embed = discord.Embed(title=f'Suggestion Implimented', colour=discord.Colour(12390624), description=f'{embed.description}')
        embed.set_author(name=f'{name}', icon_url=f'{name.avatar_url}')
        embed.add_field(name=f'Information from {user.name}:', value=f'{reason}')
        embed.set_footer(text=f'User ID: {name.id}')
        try:
            await message.edit(embed=embed)
        except:
            await ctx.send(f':x: I cannot find that suggestion.')
            return
        await ctx.send(f':white_check_mark: Marked the suggestion ({message_id}) as implemented.')
        name_embed = discord.Embed(title=f'Suggestion Implimented', colour=discord.Colour(12390624), description=f'{embed.description}')
        name_embed.set_author(name=f'{name}', icon_url=f'{name.avatar_url}')
        name_embed.add_field(name=f'Information from {user.name}:', value=f'{reason}')
        await name.send(f'Hey {name.mention}, {user} just marked your suggestion as implemented.', embed=name_embed)
        try:
            await message.clear_reactions()
        except:
            pass

    @commands.command()
    @commands.has_role(717112726412984398)
    async def comment(self, ctx, message_id, *, comment):
        """ Add a comment on a suggestion. """
        message_id = int(message_id)
        guild = self.bot.get_guild(717112726408921218)
        channel = guild.get_channel(717112726538944515)
        try:
            message = await channel.fetch_message(message_id)
        except:
            await ctx.send(f':x: I cannot find that suggestion.')
            return
        content = message.embeds
        for embed in content:
            user = ctx.author
            footer = embed.footer
            footer = str(footer)
            footer = footer.replace("EmbedProxy(text='User ID: ", '')
            footer = footer.replace("')", '')
            name = self.bot.get_user(int(footer))
        embed = discord.Embed(title=f'Suggestion from {name}', colour=discord.Colour(7506394), description=f'{embed.description}')
        embed.set_author(name=f'{name}', icon_url=f'{name.avatar_url}')
        embed.add_field(name=f'Comment from {user.name}:', value=f'{comment}')
        embed.set_footer(text=f'User ID: {name.id}')
        try:
            await message.edit(embed=embed)
        except:
            await ctx.send(f':x: I cannot find that suggestion.')
            return
        await ctx.send(f':white_check_mark: Added comment to suggestion.')
        name_embed = discord.Embed(title=f'Suggestion from {name}', colour=discord.Colour(7506394), description=f'{embed.description}')
        name_embed.set_author(name=f'{name}', icon_url=f'{name.avatar_url}')
        name_embed.add_field(name=f'Comment from {user.name}:', value=f'{comment}')
        await name.send(f'Hey {name.mention}, {user} just added a comment on your suggestion.', embed=name_embed)

def setup(bot):
    bot.add_cog(Special(bot))
