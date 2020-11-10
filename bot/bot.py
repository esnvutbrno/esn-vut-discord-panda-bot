import re
from random import choice

from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from . import logger

# https://cs.wiktionary.org/wiki/%C5%BEena
# + pandí
EYES_REGEX = re.compile(r'(^| )pand(a|y|e|ě|u|o|ou|am|ám|ach|ách|ami|i|í|ich|ích)?( |\?|!|$)', re.IGNORECASE)

class Bot(commands.Bot):
    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        await self.on_message_seen(ctx)
        await self.invoke(ctx)

    async def on_message_seen(self, ctx: Context):
        message: Message = ctx.message

        un_prefixed_content: str = message.content[len(ctx.prefix or ''):]

        if EYES_REGEX.search(un_prefixed_content):
            await message.add_reaction(choice(('👀', '😎', '🤓', '👁️', '🕶️', '🙄')))
