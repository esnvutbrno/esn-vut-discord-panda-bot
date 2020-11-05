from _operator import attrgetter
from builtins import map

from discord import VoiceChannel, Message, Role, HTTPException
from discord.ext.commands import Context

from .. import bot, logger
from ..checks import check_if_has_any_of_roles

has_sf_permission = check_if_has_any_of_roles({'Board', 'Coordinator'})


@bot.group(
    description='Module for controlling the Speedfriending event.',
    brief='Speedfriending module',
    usage='<subcommand>',
)
async def sf(ctx: Context):
    logger.warning('Unhandled message: %s.', ctx.message.content)

    if ctx.invoked_subcommand is None:
        await ctx.message.add_reaction('⁉️')


@sf.command(
    name='collect',
    brief='Collects members in role to one voice channel',
    usage='<user-role-to-collect> <target-voice-channel>',
    description='Finds all online member in role with ACTIVE call (specified by @tagged role) and moves them to one '
                'specific voice channel (specified by name w/o #).',
)
@has_sf_permission
async def move(ctx: Context, role_to_collect: Role, collect_where: VoiceChannel):
    moved = set()
    not_moved = set()

    for m in role_to_collect.members:
        try:
            await m.move_to(collect_where)
            moved.add(m)
        except HTTPException as e:
            not_moved.add(m)

    m: Message = ctx.message
    await m.add_reaction('👍')

    quote = f'> `{m.content}`\n'

    if moved:
        await ctx.send(f'{quote} Found {len(moved)} members were moved to {collect_where.mention}: '
                       f'{", ".join(map(attrgetter("nick"), moved))}.')

    if not_moved:
        await ctx.send(f'{quote} Unfortunately {len(not_moved)} members were not moved: '
                       f'{", ".join(map(attrgetter("nick"), not_moved))}.')

    if not (moved or not_moved):
        await ctx.send(f'{quote} No members in role {role_to_collect.mention} found.')