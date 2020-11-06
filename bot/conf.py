import os
from os.path import dirname

PROJECT_DIR = os.path.join(dirname(__file__), '..')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

PANDA_EMOJI = '<:panda:772918048892911617>'
BOT_COMMAND_PREFIX = ('panda? ', 'panda?', 'panda! ', 'panda!', 'panda ', 'p! ', 'p!', 'p? ', 'p?')
BOT_DESCRIPTION = '''Hello, I am Panda!\n'''
LOGGER_NAME = 'panda-bot'

MEMES_DIR = '/panda-bot/memes/'

PANDA_LOGO_IMAGE_PATH = os.path.join(DATA_DIR, 'panda.png')

PANDA_BOT_URL = 'https://github.com/thejoeejoee/esn-vut-discord-panda-bot'
DEFAULT_REPLY_COLOR = 0xcc3300

SAD_REACTION_EMOJIS = tuple(set('😐 😒 🙄 😔 😕 😟 ☹️ 🙁 😟 😢 😞'.split(' ')))