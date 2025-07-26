import discord
import subprocess
import os
import logging

# todo: refacor
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
LLM_COMMAND = 'uv run llm --key $LLM_API_KEY --model $LLM_MODEL'
FUNCTION_ARG = '--functions tools/google_calendar.py'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

## Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s     %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

_log = logging.getLogger(__name__)

@client.event
async def on_ready():
    _log.info('watari logged in.')

@client.event
async def on_message(message: discord.Message):
    # Ignore messages from the bot itself
    if message.author.bot: return
    _log.info(f"{message.author.global_name}({message.author.name}): {message.content}")

    try:
        command = f'{LLM_COMMAND} {FUNCTION_ARG} \'{message.content}\''
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10, cwd='.')
        await message.channel.send(f"{result.stdout.strip()}")
    except subprocess.TimeoutExpired:
        await message.channel.send("Command timed out")
    except Exception as e:
        _log.error(f"{e}")
        await message.channel.send(f"ERROR")

client.run(TOKEN)
