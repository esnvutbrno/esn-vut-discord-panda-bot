import logging

import discord
from decouple import AutoConfig
from discord.ext import commands

config = AutoConfig()

logging.basicConfig(level=config('LOG_LEVEL', cast=int, default=logging.INFO))

logger = logging.getLogger(__name__)

description = '''Hello, I am Panda!\n'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=('panda? ', 'panda?', 'panda! ', 'panda!', 'panda '),
    description=description,
    intents=intents
)

from .main import main

__all__ = ['main', 'bot', 'config', 'logger']
