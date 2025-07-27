import discord
from discord.ext import commands


from core.cogs.ErrorDefinitions import *




class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
    
    
    
    
    @commands.slash_command(
        name = "stats",
        description = "Stats and general info about the bot!")
    async def itemSearchCommand(self,
                          ctx: discord.ApplicationContext):
        appInfo = await self.bot.application_info()
        embed = discord.Embed(colour=0x3c7186)

        embed.add_field(name="Bot Owner",
                        value=f"{appInfo.owner.mention}",
                        inline=False)
        embed.add_field(name="Latency",
                        value=f"{round(self.bot.latency*1000, 2)}ms",
                        inline=False)
        embed.add_field(name="Guild Count",
                        value=f"{appInfo.approximate_guild_count}",
                        inline=True)
        embed.add_field(name="User Count",
                        value=f"{appInfo.approximate_user_install_count}",
                        inline=True)
        
        
        await ctx.respond(embed = embed)

    
    
    
def setup(bot: discord.Bot):
    bot.add_cog(Misc(bot))