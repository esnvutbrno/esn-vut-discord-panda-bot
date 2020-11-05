from discord import VoiceChannel, Member
from discord.ext.commands import Context

from . import bot


@bot.group(description='Module for controlling the Speedfriending event.', brief='Use for Speedfriending event.')
async def sf(ctx):
    pass


@sf.command(name='move')
async def move(ctx: Context, who: Member, where: VoiceChannel):
    await who.move_to(where)
    await ctx.send(f'{who} moved to {where}')
