import discord
from discord.ext import commands


from core.cogs.ErrorDefinitions import *
from core.db import getItemListTabComplete, getItemList, getCrateList, getTagList, addOneToItemCounter, getItemCounter, getGroupList, getMiscItemList
from core.utils import symbolsToRemove, updateFromSite, buildPopularityPaginator
from core.models.Item import Item
from core.models.MiscItem import MiscItem
from typing import List, Tuple


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
    
    @commands.slash_command(
        name = "popularity",
        description = "Shows a list of some of the most popular searched items!")
    async def topItems(self,
                       ctx: discord.ApplicationContext):   
        currentItemCounter = await getItemCounter()
        pageList = []
        
        returnText = "```ansi\n"
        if currentItemCounter:
            mostPopular = list(dict(sorted(currentItemCounter.items(), key=lambda item: item[1])).keys())
            mostPopular.reverse()
            for counter, itemName in enumerate(mostPopular, 1):
                prettyName = itemName
                for symbol in symbolsToRemove:
                    prettyName = prettyName.replace(f"{symbol} ", "").replace(f" {symbol}", "")
                potentialAddition = f"\u001b[0;32m{counter:>2}\u001b[0;0m - \u001b[0;35m{prettyName:<36}\u001b[0;0m (\u001b[0;36m{currentItemCounter[itemName]}\u001b[0;0m)\n"
                if len(returnText + potentialAddition) <= 4096:
                    returnText += potentialAddition
                else: 
                    returnText += "```"
                    pageList.append(returnText)
                    returnText = f"```ansi\n{potentialAddition}"
            if not returnText.endswith("```"):
                returnText += "```"
                pageList.append(returnText)
        else:
            returnText += "No items searched yet!```"
        embeds = []
        for page in pageList:
            embed = discord.Embed(color=0x3c7186)
            embed.title = "Most popular searches!"
            embed.description = page
            embeds.append(embed)
        paginator = buildPopularityPaginator(embeds)
        await paginator.respond(ctx.interaction, ephemeral = False)
        
    @commands.slash_command(
        name = "stats",
        description = "Stats and general info about the bot!")
    async def itemSearchCommand(self,
                          ctx: discord.ApplicationContext):
        appInfo = await self.bot.application_info()
        embed = discord.Embed(colour=0x3c7186)

        embed.add_field(name="Bot Manager",
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
        searchCounter = 0
        currentItemCounter = await getItemCounter()
        if currentItemCounter:
            for itemName in currentItemCounter.keys():
                searchCounter += currentItemCounter[itemName]
            
            embed.add_field(name="Search Count",
                            value=f"{searchCounter}",
                            inline=True)
        
        
        await ctx.respond(embed = embed)

    @commands.slash_command(
        name = "refresh",
        description = "Bot manager can refresh item data with this command.")
    async def refreshData(self,
                          ctx: discord.ApplicationContext):
        await ctx.defer()
        appInfo = await self.bot.application_info()
        if ctx.author.id == appInfo.owner.id or ctx.author.id == 845863303258570782: # Bot owner or Roland_Gaymer
            missingPics, missingMiscPics = await updateFromSite()
            print(f"{appInfo.owner.name} refreshed item data.")
            itemList = await getItemList()
            crateList = await getCrateList()
            tagList = await getTagList()
            groupList = await getGroupList()
            miscItemList = await getMiscItemList()
                
            embed = discord.Embed(title="Data Refreshed", colour=0x3c7186)
            ret = "The following items have not had images generated yet, and will thus be excluded.```"
            if missingPics:
                for item in missingPics:
                    ret += f"\n{item.id} - {item.ItemName}"
                embed.description = ret
            if missingMiscPics:
                for item in missingMiscPics:
                    ret += f"\n{item.id} - {item.ItemName}"
            if missingMiscPics or missingPics:
                ret += "```"
                embed.description = ret
            if itemList:
                embed.add_field(name="Item Count:",
                                value=f"{len(itemList)}",
                                inline=False)
            if crateList:
                embed.add_field(name="Crate Count:",
                                value=f"{len(crateList)}",
                                inline=False)
            if tagList:
                embed.add_field(name="Tag Count:",
                                value=f"{len(tagList)}",
                                inline=False)
            if groupList:
                embed.add_field(name="Miscellaneous Group Count:",
                                value=f"{len(groupList)}",
                                inline=False)
            if miscItemList:
                embed.add_field(name="Miscellaneous Item Count:",
                                value=f"{len(miscItemList)}",
                                inline=False)
            embed.set_footer(text=f"{ctx.author.name}",
                            icon_url=f"{ctx.author.display_avatar.url}")
            
        else:
            embed = discord.Embed(title="Unauthorized user.", colour=0x3c7186)
            embed.add_field(name="Reason:",
                            value=f"You are not {appInfo.owner.mention}, thus you cannot use this command.",
                            inline=False)
            embed.set_footer(text=f"{appInfo.owner.name}",
                            icon_url=f"{appInfo.owner.display_avatar.url}")
        await ctx.followup.send(embed = embed)
    
    
def setup(bot: discord.Bot):
    bot.add_cog(Misc(bot))