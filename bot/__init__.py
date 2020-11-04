import logging

import discord
from decouple import AutoConfig
from discord.ext import commands

config = AutoConfig()

logging.basicConfig(level=config('LOG_LEVEL', cast=int, default=logging.INFO))

logger = logging.getLogger(__name__)

description = '''Hello, I am Panda! :panda: How can I help you?'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='panda ', description=description, intents=intents)

from .bot import main
