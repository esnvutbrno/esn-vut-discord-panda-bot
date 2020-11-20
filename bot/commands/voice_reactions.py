import asyncio
from random import choice
from typing import Optional

from discord import Member, VoiceState, VoiceChannel, FFmpegPCMAudio, PCMVolumeTransformer

from . import bot
from .. import logger
from ..conf import VoiceReactionsConf


@bot.event
async def on_voice_state_update(who: Member, from_state: VoiceState, to_state: VoiceState):
    logger.info(
        'Voice state update %s: %s -> %s',
        who.nick,
        from_state.channel,
        to_state.channel
    )

    if who == bot:
        return

    if to_state.channel == from_state.channel:
        # deaf / mute / whatevent, no channel change
        return

    to_channel: Optional[VoiceChannel] = to_state.channel

    if not to_channel:
        # TODO: bye bye
        return

    if to_channel.name not in VoiceReactionsConf.INCLUDE_CHANNELS:
        return

    guild = to_channel.guild
    if guild.voice_client is not None:
        await guild.voice_client.move_to(to_channel)
    else:
        await to_channel.connect()
        
    await asyncio.sleep(1)
    source = PCMVolumeTransformer(FFmpegPCMAudio(choice(VoiceReactionsConf.WELCOME_REACTIONS)))
    guild.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
