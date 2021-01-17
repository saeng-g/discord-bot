import discord
import random
from discord.ext import commands
import json

CONFIG_FILE = 'config.json'
CREDENTIALS_KEY = 'credentials'
DISCORD_TOKEN_KEY = 'discord_token'
with open(CONFIG_FILE) as f:
    credentials = json.loads(f.read())[CREDENTIALS_KEY]
discord_token = credentials[DISCORD_TOKEN_KEY]

trivia_status = 0
k = []
client = commands.Bot(command_prefix='.kybot.', intents=discord.Intents.all())

@client.event
async def on_connect():
    print(f'{client.user} has connected to Discord')

@client.event
async def on_ready():
    print(f'{client.user} is ready')

@client.event
async def on_member_join(member):
    print(f'{member} joined the server')
    await member.guild.system_channel.send('hi')

@client.event
async def on_member_remove(member):
    print(f'{member} left the server')
    await member.guild.system_channel.send('bye')

@client.command(name='trivia')
async def trivia(ctx, trivia_name=''):
    global trivia_status
    trivia_status = 1
    trivia_qna = json.loads(open(f'trivia{trivia_name}.json').read())
    random.shuffle(trivia_qna)
    for q in trivia_qna:
        qstr = f"{q['question']}\n"
        for k in sorted(q['choices'].keys()):
            qstr += f"\n  {k} - {q['choices'][k]}"
        embed = discord.Embed(title='Poll', description=qstr, colour=discord.Colour.red())
        msg = await ctx.send(embed=embed)
        emoji_str_codes = [b"\xf0\x9f\x87\xa6".decode(),
            b"\xf0\x9f\x87\xa7".decode(),
            b"\xf0\x9f\x87\xa8".decode(),
            b"\xf0\x9f\x87\xa9".decode(),
            b"\xf0\x9f\x87\xaa".decode(),
            b"\xf0\x9f\x87\xab".decode(),
            b"\xf0\x9f\x87\xac".decode()
        ][:len(q['choices'].keys())]
        for emoji in emoji_str_codes:
            await msg.add_reaction(emoji)

client.run(discord_token)
print('running')