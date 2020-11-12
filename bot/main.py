from datetime import time, datetime

import discord

from . import bot, config, logger
# noinspection PyUnresolvedReferences
from .commands import motivation, welcome, speedfriending
from .conf import DEFAULT_BOT_PREFIX
from .error_handler import CommandErrorHandler


@bot.event
async def on_ready():
    logger.info('Logged in as %s: %s.', bot.user.name, bot.user.id)

    await bot.change_presence(
        activity=discord.Activity(
            name=f'{DEFAULT_BOT_PREFIX} | \n{config("ENVIRONMENT")}@{config("VERSION")}',
            type=discord.ActivityType.listening,
            timestamps=dict(
                start=datetime.now()
            )
        )
    )


def main():
    bot.add_cog(CommandErrorHandler(bot))
    bot.run(config('BOT_TOKEN'))


__all__ = ['main']
