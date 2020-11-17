import contextlib
import random
from random import choice
from typing import Tuple, Any, Union, Optional, Iterable

from discord import Embed, File, Member
from discord.ext.commands import Context, MemberConverter as OriginalMemberConverter, MemberNotFound

from bot.conf import PANDA_LOGO_IMAGE_PATH, PANDA_BOT_URL, DEFAULT_REPLY_COLOR, SAD_REACTION_EMOJIS, \
    ERROR_GIFS


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
        files: Optional[Iterable[File]] = None,
        image_url: Optional[str] = None,
        reaction='✅'
) -> Tuple[Embed, Any]:
    me = ctx.me
    embed = Embed(
        title=title,
        description=description,
        color=me.top_role.color if isinstance(me, Member) else DEFAULT_REPLY_COLOR,
        image_url=image_url,
    )

    logo = File(PANDA_LOGO_IMAGE_PATH, filename='panda.png')
    embed.set_author(name=author_name or 'Panda', icon_url="attachment://panda.png", url=PANDA_BOT_URL)

    async def send_callback():
        await ctx.message.add_reaction(reaction)
        return await ctx.send(embed=embed, files=(logo, *(files or ())))

    return embed, send_callback


def reply_error_embed(ctx: Context, error: Union[Exception, str]) -> Tuple[Embed, Any]:
    if random.random() > .8:
        with local_seed(hash(ctx.message.content)):
            gif = choice(ERROR_GIFS)

        error_gif = File(gif, filename='error-gif.gif')
        image_url = "attachment://error-gif.gif" if random.random() > 0 else None
    else:
        error_gif = image_url = None

    return reply_embed(
        ctx,
        description=f'> {ctx.message.content}\n{error}{"" if str(error).endswith(".") else "."}'
                    f' {random.choice(SAD_REACTION_EMOJIS)}',
        author_name=f'Panda is {random.choice("disappointed sad frustrated".split())}',
        reaction='🛑',
        image_url=image_url,
        files=(error_gif,) if image_url else None
    )


class MemberIncludingAuthorConverter(OriginalMemberConverter):
    MYSELFS = ('me',)

    async def convert(self, ctx: Context, argument):
        print('conv', argument)
        try:
            return await super().convert(ctx, argument)
        except MemberNotFound:
            if argument in self.MYSELFS:
                return ctx.author

        raise MemberNotFound(argument)
