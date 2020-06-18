import discord, json
from discord.ext import commands
error_icon = 'https://cdn.discordapp.com/emojis/678014140203401246.png?v=1'
Client = discord.Client()

initial_extensions = ['admin', 'moderation', 'misc', 'special']

File = open('/root/Bot_Shop/info.json', 'r').read()# You may need to put the full path to the file here.
data = json.loads(File)
botid = data['botid']

async def get_prefix(bot, message):
  return [data['prefix'], f'<@!{botid}> ', f'<@{botid}> ', f'<@{botid}>', f'<@!{botid}>']

client = commands.Bot(command_prefix=get_prefix, description=data['help_message'], case_insensitive=True)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f'Bot Shop: {extension} could not be loaded!\n{type(e).__name__}: {e}')

@client.event
async def on_ready():
    # (activity=discord.Game(name="a game"))
    # (activity=discord.Streaming(name="My Stream", url=my_twitch_url))
    # (activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
    # (activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
    await client.change_presence(activity=discord.Game(type=0, name=f'with Bots and New Code :robot:'), status=discord.Status.online)
    print(f'"{client.user.name}" is ready to use.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ExtensionNotLoaded) or isinstance(error, commands.ExtensionAlreadyLoaded) or isinstance(error, commands.ExtensionFailed) or isinstance(error, commands.ExtensionNotFound) or isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'**:bangbang: ERROR :bangbang:**\n{error}')
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send('**:bangbang: ERROR :bangbang:**\nThis command cannot be used in DMs!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f'**:bangbang: ERROR :bangbang:**\nYou do not have the required permissions to do that command.\nMissing Permission: `{error.missing_perms}`')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f'**:bangbang: ERROR :bangbang:**\nI do not have the required permissions to do that command.\nMissing Permission: `{error.missing_perms}`')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':x: You don\'t have permission to do this command!')
    else:
        await ctx.send(f'**:bangbang: ERROR :bangbang:**\n{error}\n*This seems to be an error with the code. Please contact the bot owner about this!*')

client.run(data['token'])
