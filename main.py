import discord
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Starting
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Member Join
@client.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if welcome_channel:
        await welcome_channel.send(f'Welcome {member.mention} to the server!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # word moderation
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f'{message.author.mention}, please do not use that word!')


    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello World! I am alive!')
    
    # Help 
    if message.content.startswith(f'{PREFIX}help'):
        await message.channel.send('Hello World! I am alive!')
    
    # Music
    if message.content.startswith(f'{PREFIX}music'):
        await message.channel.send('Hello World! I am alive!')
    
    # Meme 
    if message.content.startswith(f'{PREFIX}help'):
        await message.channel.send('Hello World! I am alive!')

client.run(TOKEN)