import discord
from discord import Member, Guild, TextChannel

from . import bot, Optional
from ..conf import PANDA_EMOJI


@bot.event
async def on_member_join(member: Member):
    """
    Sends welcome message for new user to general channel.
    """
    if not member.guild or not member.guild.system_channel:
        return

    g: Guild = member.guild

    rules: Optional[TextChannel] = discord.utils.get(g.channels, name='rules')

    await g.system_channel.send(
        f'Cheers {member.mention}, **Panda from ESN VUT Brno** welcomes you here! {PANDA_EMOJI}\n'
        f'*Shhh, I recommend you to see the {rules.mention if rules else "#rules"} channel.*'
    )
