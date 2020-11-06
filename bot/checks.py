from discord.ext.commands import has_role, has_any_role

board_role_required = has_role('Board')
esner_role_required = has_role('ESNer')

board_or_coord_role_required = has_any_role('Board', 'Coordinator')
