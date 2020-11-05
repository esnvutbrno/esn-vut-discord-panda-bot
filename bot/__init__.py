import logging

import discord
from decouple import AutoConfig
from discord.ext import commands

from .conf import BOT_COMMAND_PREFIX, BOT_DESCRIPTION, LOGGER_NAME

config = AutoConfig()

logging.basicConfig(level=config('LOG_LEVEL', cast=int, default=logging.INFO))

logger = logging.getLogger(LOGGER_NAME)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=BOT_COMMAND_PREFIX,
    description=BOT_DESCRIPTION,
    intents=intents
)

from .main import main

__all__ = ['main', 'bot', 'config', 'logger']
