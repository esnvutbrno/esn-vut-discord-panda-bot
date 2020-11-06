from discord import TextChannel
from discord.ext.commands import Context

from .. import bot
from ..checks import board_or_coord_role_required


@bot.command(
    description='Sends a message to specific channel',
    brief='Do you want to send a message?',
    usage='<#target-channel> <message>'
)
@board_or_coord_role_required
async def send(ctx: Context, where: TextChannel, *, what: str):
    await where.send(what)
