import discord

from . import bot, config, logger
# noinspection PyUnresolvedReferences
from .commands import motivation, welcome, speedfriending
from .error_handler import CommandErrorHandler


@bot.event
async def on_ready():
    logger.info('Logged in as %s: %s.', bot.user.name, bot.user.id)

    await bot.change_presence(
        activity=discord.Activity(
            name=f'panda!',
            type=discord.ActivityType.listening
        )
    )


def main():
    bot.add_cog(CommandErrorHandler(bot))
    bot.run(config('BOT_TOKEN'))


__all__ = ['main']
