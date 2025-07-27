import discord
from discord.ext import commands

from core.cogs.ErrorDefinitions import *

class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
    
    @commands.Cog.listener()
    async def on_application_command_error(
            self,
            ctx: discord.ApplicationContext,
            error: discord.DiscordException
        ):
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.command:
                await ctx.respond(f"You are currently on cooldown with `/{ctx.command.name}`! Try again in `{round(error.retry_after, 1)}` seconds.")
        elif isinstance(error, NoItemsInDatabaseError):
            await ctx.respond("No items found in the Database. Please report this to staff.")
        elif isinstance(error, ItemNotInDatabaseError):
            if ctx.selected_options:
                await ctx.respond(f"Item: `{ctx.selected_options[0]["value"]}` is not valid. Please use the Auto Complete suggestions!")
        elif isinstance(error, NoTagsInDatabaseError):
            await ctx.respond(f"No tags found in the Database. Please report this to staff.")
        elif isinstance(error, TagNotInDatabaseError):
            if ctx.selected_options:
                await ctx.respond(f"Tag: `{ctx.selected_options[0]["value"]}` is not valid. Please use the Auto Complete suggestions!")
        elif isinstance(error, NoResultsFoundError):
            if ctx.selected_options:
                await ctx.respond(f"Term: `{ctx.selected_options[0]["value"]}` had no results found.")
        elif isinstance(error, NoCratesInDatabaseError):
            await ctx.respond("No crates found in the Database. Please report this to staff.")
        elif isinstance(error, CrateNotInDatabaseError):
            if ctx.selected_options:
                await ctx.respond(f"Crate: `{ctx.selected_options[0]["value"]}` is not valid. Please use the Auto Complete suggestions!")
        else:
            raise error
    
def setup(bot: discord.Bot):
    bot.add_cog(ErrorCog(bot))