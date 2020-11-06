import re
from _operator import attrgetter
from builtins import map
from operator import attrgetter
from random import shuffle
from typing import Dict, Set, List, Tuple

from discord import VoiceChannel, Message, Role, HTTPException, CategoryChannel, Member
from discord.ext.commands import Context

from .exceptions import NoUsersFoundInRole, NoNumberedVoiceChannelsInCategory
from .. import bot
from ..checks import board_or_coord_role_required
from ..utils import reply_embed

has_sf_permission = board_or_coord_role_required

VOICE_CHANNEL_TARGETS_RE = re.compile(r'.*\d+$')


@bot.group(
    description='Module for controlling the Speedfriending event.',
    brief='Speedfriending module',
    usage='<subcommand>',
)
@has_sf_permission
async def sf(ctx: Context):
    if ctx.invoked_subcommand is None:
        await ctx.send_help(sf)


@sf.command(
    name='collect',
    brief='Collects members in role to one voice channel',
    usage='<user-role-to-collect> <target-voice-channel>',
    description='Finds all online member in role with ACTIVE call (specified by @tagged role) and moves them to one '
                'specific voice channel (specified by name w/o #).',
)
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
    embed, send = reply_embed(ctx=ctx, title='Speedfriending collect', description=f'> `{m.content}`')

    if moved:
        embed.add_field(
            name='Success',
            value=f'Found {len(moved)} members were moved to {collect_where.mention}: ' \
                  f'{", ".join(filter(None, map(attrgetter("display_name"), moved)))}.'
        )

    if not_moved:
        embed.add_field(
            name='Fail',
            value=f'Unfortunately {len(not_moved)} members were not moved: ' \
                  f'{", ".join(filter(None, map(attrgetter("display_name"), not_moved)))}.'
        )

    if not (moved or not_moved):
        raise NoUsersFoundInRole(role_to_collect.mention)

    await send()


@sf.command(
    name='split',
    brief='Splits members in role equally to multiple voice channels',
    usage='<user-role-to-split> <target-category>',
    description='Finds all online member in role with ACTIVE call (specified by @tagged role) and splits them equally'
                'to all voice channels in category (by name) ending with NUMBER.',
)
async def split(ctx: Context, role_to_split: Role, category: CategoryChannel):
    not_moved = set()
    members_to_split: List[Member] = role_to_split.members

    if not members_to_split:
        raise NoUsersFoundInRole(role_to_split.mention)

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
        raise NoNumberedVoiceChannelsInCategory(category.name)

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

    embed, send = reply_embed(
        ctx=ctx,
        title="Speedfriending split",
        description=f"Success, {len(members_to_split) - len(not_moved)} members in role {role_to_split.mention}"
                    f"has been split into {len(results)} channels:"
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

    await send()
