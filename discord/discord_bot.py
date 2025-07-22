import discord
import datetime
import subprocess
import os

# todo: refacrot
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
LLM_COMMAND = 'uv run llm --key $LLM_API_KEY --model $LLM_MODEL'
FUNCTION_ARG = '--functions tools/google_calendar.py'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('watari logged in.')

@client.event
async def on_message(message: discord.Message):
    # Ignore messages from the bot itself
    if message.author.bot:
        return
    
    # log
    print(f"[{datetime.datetime.now()}] {message.author.global_name}({message.author.name}): {message.content}")
    
    try:
        # [!WARNING!] There are security risks in executing shell commands from user input (OS command injection).
        command = f'{LLM_COMMAND} {FUNCTION_ARG} \'{message.content}\''
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10, cwd='.')
        await message.channel.send(f"{result.stdout.strip()}")
    except subprocess.TimeoutExpired:
        await message.channel.send("Command timed out")
    except Exception as e:
        print(f"[ERROR] {e}")
        await message.channel.send(f"ERROR")

client.run(TOKEN)
