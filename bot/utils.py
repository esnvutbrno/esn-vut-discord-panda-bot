import contextlib
import random
from typing import Tuple, Any, Union, Optional

from discord import Embed, File, Member
from discord.ext.commands import Context

from bot.conf import PANDA_LOGO_IMAGE_PATH, PANDA_BOT_URL, DEFAULT_REPLY_COLOR, SAD_REACTION_EMOJIS


@contextlib.contextmanager
def local_seed(seed):
    """
    Sets specific seed for random module only for inner code.
    """
    state = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(state)


def reply_embed(
        ctx: Context,
        title=None,
        description=None,
        author_name: Optional[str] = None,
        reaction='✅'
) -> Tuple[Embed, Any]:
    me = ctx.me
    embed = Embed(
        title=title,
        description=description,
        color=me.top_role.color if isinstance(me, Member) else DEFAULT_REPLY_COLOR,
    )

    logo = File(PANDA_LOGO_IMAGE_PATH, filename='panda.png')
    embed.set_author(name=author_name or 'Panda', icon_url="attachment://panda.png", url=PANDA_BOT_URL)

    async def send_callback():
        await ctx.message.add_reaction(reaction)
        return await ctx.send(embed=embed, file=logo)

    return embed, send_callback


def reply_error_embed(ctx: Context, error: Union[Exception, str]) -> Tuple[Embed, Any]:
    return reply_embed(
        ctx,
        description=f'> {ctx.message.content}\n{error}{"" if str(error).endswith(".") else "."}'
                    f' {random.choice(SAD_REACTION_EMOJIS)}',
        author_name=f'Panda is {random.choice("disappointed sad frustrated".split())}',
        reaction='🛑'
    )
