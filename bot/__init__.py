import logging

import discord
from decouple import AutoConfig

from .conf import BOT_COMMAND_PREFIX, BOT_DESCRIPTION, LOGGER_NAME

config = AutoConfig()

logging.basicConfig(level=config('LOG_LEVEL', cast=int, default=logging.INFO))

logger = logging.getLogger(LOGGER_NAME)

from .bot import Bot

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = Bot(
    command_prefix=BOT_COMMAND_PREFIX,
    description=BOT_DESCRIPTION,
    intents=intents
)

from .main import main

__all__ = ['main', 'bot', 'config', 'logger']
