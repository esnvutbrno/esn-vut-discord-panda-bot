import re
from _operator import attrgetter
from builtins import map
from operator import attrgetter
from random import shuffle, choice
from typing import Dict, Set, Iterable, List, Tuple

from discord import VoiceChannel, Message, Role, HTTPException, CategoryChannel, Embed, Member
from discord.ext.commands import Context

from .. import bot, logger
from ..checks import check_if_has_any_of_roles

has_sf_permission = check_if_has_any_of_roles({'Board', 'Coordinator'})

VOICE_CHANNEL_TARGETS_RE = re.compile(r'.*\d+$')


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
async def collect(ctx: Context, role_to_collect: Role, collect_where: VoiceChannel):
    moved = set()
    not_moved = set()

    for m in role_to_collect.members:
        try:
            await m.move_to(collect_where)
            moved.add(m)
        except HTTPException as e:
            not_moved.add(m)

    m: Message = ctx.message
    await m.add_reaction('✅')

    quote = f'> `{m.content}`\n'

    if moved:
        await ctx.send(f'{quote} Found {len(moved)} members were moved to {collect_where.mention}: '
                       f'{", ".join(map(attrgetter("nick"), moved))}.')

    if not_moved:
        await ctx.send(f'{quote} Unfortunately {len(not_moved)} members were not moved: '
                       f'{", ".join(map(attrgetter("nick"), not_moved))}.')

    if not (moved or not_moved):
        await ctx.send(f'{quote} No members in role {role_to_collect.mention} found.')


@sf.command(
    name='split',
    brief='Splits members in role equally to multiple voice channels',
    usage='<user-role-to-split> <target-category>',
    description='Finds all online member in role with ACTIVE call (specified by @tagged role) and splits them equally'
                'to all voice channels in category (by name) ending with NUMBER.',
)
@has_sf_permission
async def split(ctx: Context, role_to_split: Role, category: CategoryChannel):
    not_moved = set()
    members_to_split: List[Member] = role_to_split.members

    if not members_to_split:
        await ctx.send(f'Sorry, no members found in role {role_to_split.name}.')
        return

    shuffle(members_to_split)

    # type: Tuple[VoiceChannel]
    voice_channels = tuple(
        filter(
            lambda c: VOICE_CHANNEL_TARGETS_RE.match(c.name),
            category.voice_channels
        )
    )
    voice_channels_count = len(voice_channels)

    if not voice_channels_count:
        await ctx.send(f'Sorry, no available voice channels found in category {category.name}.\n*Maybe channels don\'t '
                       f'have the numbers?*')
        return

    results: Dict[VoiceChannel, Set[Member]] = {c: set() for c in voice_channels}

    i = 0
    for member in members_to_split:
        target_channel = voice_channels[i % voice_channels_count]
        try:
            await member.move_to(target_channel)
            results[target_channel].add(member)
            # move pointer only when user was been moved (w/o scale with forloop)
            i += 1
        except HTTPException as e:
            not_moved.add(member)

    embed = Embed(
        title="Speedfriending",
        description=f"Success, {len(members_to_split) - len(not_moved)} members in role {role_to_split.mention}"
                    f"has been split into {len(results)} channels:",
        color=ctx.me.top_role.color,
    )
    for channel, members in results.items():
        embed.add_field(
            name=f'{channel.name}',
            value=f'{", ".join(map(attrgetter("mention"), members)) or "no members"}',
            inline=False,
        )
    if not_moved:
        embed.add_field(
            name='Unable to move',
            value=', '.join(tuple(map(attrgetter('mention'), not_moved)))
        )
    await ctx.send(embed=embed)

    message: Message = ctx.message
    await message.add_reaction('✅')
