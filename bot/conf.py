import os
from functools import partial
from os import listdir
from os.path import dirname

PROJECT_DIR = os.path.join(dirname(__file__), '..')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

ASSETS_DIR = '/panda-bot/'

PANDA_EMOJI = '<:panda:772918048892911617>'
DEFAULT_BOT_PREFIX = 'panda!'
BOT_COMMAND_PREFIX = ('panda? ', 'panda?', 'panda! ', DEFAULT_BOT_PREFIX, 'panda ', 'p! ', 'p!', 'p? ', 'p?')
BOT_DESCRIPTION = '''Hello, I am Panda!\n'''
LOGGER_NAME = 'panda-bot'

MEMES_DIR = os.path.join(ASSETS_DIR, 'memes/')

PANDA_LOGO_IMAGE_PATH = os.path.join(DATA_DIR, 'panda.png')
ERROR_GIFS = tuple(map(
    partial(os.path.join, os.path.join(DATA_DIR, 'error-gifs')),
    listdir(os.path.join(DATA_DIR, 'error-gifs'))
))

PANDA_BOT_URL = 'https://github.com/thejoeejoee/esn-vut-discord-panda-bot'
DEFAULT_REPLY_COLOR = 0xcc3300

SAD_REACTION_EMOJIS = tuple(set('😐 😒 🙄 😔 😕 😟 ☹️ 🙁 😟 😢 😞'.split(' ')))


class VoiceReactionsConf:
    _BASE_REACTION_DIR = os.path.join(DATA_DIR, 'voice-reactions/')
    INCLUDE_CHANNELS = {'general'}

    _WELCOME_REACTIONS_DIR = os.path.join(_BASE_REACTION_DIR, 'welcome/')
    WELCOME_REACTIONS = tuple(map(
        partial(os.path.join, _WELCOME_REACTIONS_DIR),
        listdir(_WELCOME_REACTIONS_DIR)
    ))
