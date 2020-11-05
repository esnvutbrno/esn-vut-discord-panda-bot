from operator import attrgetter
from typing import Set

from discord import Member
from discord.ext import commands
from discord.ext.commands import Context

from bot import logger


def check_is_in_role(role: str):
    def predicate(ctx: Context):
        user: Member = ctx.message.author
        logger.info('Checking if %s (%s) is in role %s: %s', user, user.roles, role, role in user.roles)
        return role in set(map(attrgetter('name'), user.roles))

    return commands.check(predicate)


def check_if_has_any_of_roles(roles: Set[str]):
    def predicate(ctx: Context):
        user: Member = ctx.message.author
        user_roles = set(map(attrgetter('name'), user.roles))

        logger.info('Checking if %s (%s) has role from %s: %s', user, user_roles, roles, bool(roles & user_roles))
        return bool(roles & user_roles)

    return commands.check(predicate)


board_role_required = check_is_in_role('Board')
esner_role_required = check_is_in_role('ESNer')
