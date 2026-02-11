Hive Commands
-------------

Hive Commands are subclasses of :class:`cgrig.libs.command.command.CgRigCommandMaya` but are solely built around hive
operation's.
Hive api is intentionally not undoable but we do have our way's of making an operation undoable
and that's what Hive Commands are for.

The general workflow is to use the api directly for queries but for state changes use hive commands
if a hive command doesn't exist then create one see :class:`cgrig.libs.command.command.CgRigCommandMaya` for more information.




.. automodule:: cgrig.libs.commands.hive
    :members:
    :undoc-members:
    :show-inheritance:

