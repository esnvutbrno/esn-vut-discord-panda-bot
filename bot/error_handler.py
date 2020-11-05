import traceback

from discord import HTTPException
from discord.ext.commands import Cog, CommandNotFound, BadArgument, NoPrivateMessage, DisabledCommand

from bot import logger


class CommandErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
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

        ignored = (CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except HTTPException:
                pass

        elif isinstance(error, BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        else:
            logger.exception(error)

        await ctx.message.add_reaction('💀')