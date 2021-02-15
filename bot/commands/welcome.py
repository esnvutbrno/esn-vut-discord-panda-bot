from discord import Member, Guild

from . import bot
from ..conf import PANDA_EMOJI


@bot.event
async def on_member_join(member: Member):
    """
    Sends welcome message for new user to general channel.
    """
    if not member.guild or not member.guild.system_channel:
        return

    g: Guild = member.guild

    await g.system_channel.send(
        f'Cheers {member.mention}, **Panda welcomes you on {g.name} Discord! {PANDA_EMOJI}\n'
        f'*Shhh, the panel of the left offers plenty of channels of various quality, and level of fun - feel free to '
        f'explore them!*'
    )
