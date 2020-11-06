import os
from os import listdir
from random import choice

import discord
from discord.ext.commands import Context

from .. import bot
from ..conf import MEMES_DIR


@bot.command(
    description='Give me some ESN meme',
    brief='Give me meme from ESN MemeCon right now!',
)
async def meme(ctx: Context):
    memes = []
    if not (os.path.exists(MEMES_DIR) and (memes := listdir(MEMES_DIR))):
        await ctx.send(f"No memes found in my storage, sorry. 😔")
        return

    await ctx.message.add_reaction('👌')

    await ctx.send(file=discord.File(
        os.path.join(MEMES_DIR, choice(memes))
    ))
