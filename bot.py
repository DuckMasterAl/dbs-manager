import discord, json
from discord.ext import commands
error_icon = 'https://cdn.discordapp.com/emojis/678014140203401246.png?v=1'
Client = discord.Client()

initial_extensions = ['admin', 'moderation', 'misc']

File = open('/Users/duckmasteral/Documents/GitHub/discord-bot-shop/info.json', 'r').read()# You may need to put the full path to the file here.
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
            print(f'{extension} could not be loaded!\n{type(e).__name__}: {e}')

@client.event
async def on_ready():
    # (activity=discord.Game(name="a game"))
    # (activity=discord.Streaming(name="My Stream", url=my_twitch_url))
    # (activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
    # (activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
    print(f'Logged in as "{client.user.name}".\nPrefix:', data['prefix'])

client.run(data['token'])