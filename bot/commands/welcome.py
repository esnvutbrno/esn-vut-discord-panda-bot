from discord import Member

from . import bot


@bot.event
async def on_member_join(member: Member):
    pass # await member.send('Hello, I am panda!\nI\'m ')
