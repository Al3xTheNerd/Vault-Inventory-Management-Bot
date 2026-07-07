from typing import Any
from discord.ext import commands
class NoItemsInDatabaseError(commands.CommandError):
    def __init__(self, message="No Items found in the Database."):
        super().__init__(message)

class ItemNotInDatabaseError(commands.CommandError):
    def __init__(self, message = "Item not found in the Database."):
        super().__init__(message)

class NoTagsInDatabaseError(commands.CommandError):
    def __init__(self, message = "No Tags found in the Database."):
        super().__init__(message)

class TagNotInDatabaseError(commands.CommandError):
    def __init__(self, message = "Tag not found in the Database."):
        super().__init__(message)

class NoResultsFoundError(commands.CommandError):
    def __init__(self, message = "No results found."):
        super().__init__(message)

class NoCratesInDatabaseError(commands.CommandError):
    def __init__(self, message = "No crates found in the Database."):
        super().__init__(message)

class CrateNotInDatabaseError(commands.CommandError):
    def __init__(self, message = "Crate not found in the Database"):
        super().__init__(message)

class MinimumConstraintError(commands.CommandError):
    def __init__(self, message = "Must have at least 1 constraint."):
        super().__init__(message)