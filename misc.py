import discord, json, time
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """ Ping Pong! Check the Bot's Latency. """
        start = time.perf_counter()
        message = await ctx.send(f":ping_pong: Pong!\n> :heart: {round(self.bot.latency * 1000)}ms")
        end = time.perf_counter()
        await message.edit(content=f"{message.content}\n> :pencil2: {round((end - start) * 1000)}ms")

    @commands.command()
    async def invite(self, ctx):
        """ Invite the Bot to your Server! """
        File = open('/root/Bot_Shop/info.json', 'r').read()# You may need to put the full path to the file here.
        data = json.loads(File)
        await ctx.send(f'You can invite the bot here:\nhttps://discordapp.com/oauth2/authorize?client_id='+data['botid']+'&scope=bot&permissions=339014')

    @commands.command()#enabled=False)
    async def support(self, ctx):
        """ Join the Bot's Official Support Server! """
        File = open('/root/Bot_Shop/info.json', 'r').read()# You may need to put the full path to the file here.
        data = json.loads(File)
        if data['supportserver'] is None:
            await ctx.send(f':x: The Bot Owner has Not Added an Official Support Server!')
        else:
            server = data['supportserver']
            await ctx.send(f'You can join the {self.bot.user.name} Support Server Here: {server}')

def setup(bot):
    bot.add_cog(Misc(bot))
