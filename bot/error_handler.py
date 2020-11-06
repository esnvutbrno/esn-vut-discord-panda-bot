from discord import HTTPException
from discord.ext.commands import Cog, CommandNotFound, BadArgument, NoPrivateMessage, DisabledCommand, CheckFailure, \
    Context, MissingRequiredArgument, UserInputError

from bot import logger
from bot.utils import reply_error_embed


class CommandErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        error = getattr(error, 'original', error)

        if isinstance(error, (CheckFailure, CommandNotFound)):
            embed, send = reply_error_embed(ctx=ctx, error=error)
            await send()

        elif isinstance(error, DisabledCommand):
            embed, send = reply_error_embed(ctx=ctx, error=f'{ctx.command} has been disabled.')
            await send()

        elif isinstance(error, NoPrivateMessage):
            embed, send = reply_error_embed(ctx=ctx, error=error)
            await ctx.message.add_reaction('🛑')

            try:
                await ctx.author.send(embed=embed)
            except HTTPException:
                pass

        elif isinstance(error, UserInputError):
            embed, send = reply_error_embed(ctx=ctx, error=error)
            await send()

        elif isinstance(error, BadArgument):
            logger.warning('Bad argument: %s', error)

        else:
            logger.exception(error)
