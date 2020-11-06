from discord.ext.commands import UserInputError


class NoUsersFoundInRole(UserInputError):
    def __init__(self, role=None, message=None, *args):
        super().__init__(message or f'No users found in role {role}.', *args)


class NoNumberedVoiceChannelsInCategory(UserInputError):
    def __init__(self, category=None, message=None, *args):
        super().__init__(
            message or f'Sorry, no available voice channels found in category {category}.\n*Maybe channels don\'t '
                       f'have the numbers?*',
            *args
        )
