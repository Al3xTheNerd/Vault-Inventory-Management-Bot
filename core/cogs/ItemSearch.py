import discord
from discord.ext import commands
from discord.commands import option, SlashCommandGroup


from core.db import getItemListTabComplete, getItemList, getCrateList, getTagList
from core.models.Item import itemToEmbed
from core.cogs.ErrorDefinitions import *
from core.utils import buildPaginator

async def itemNameTabComplete(ctx: discord.AutocompleteContext):
    itemsList = await getItemListTabComplete()
    if itemsList:
        return [item for item in itemsList if ctx.value.lower() in item.lower()]
    return None

async def tagNameTabComplete(ctx: discord.AutocompleteContext):
    tagsList = await getTagList()
    if tagsList:
        return [tag for tag in tagsList if ctx.value.lower() in tag.lower()]
    return None

async def crateNameTabComplete(ctx: discord.AutocompleteContext):
    cratelist = await getCrateList()
    if cratelist:
        return [crate.CrateName for crate in cratelist if ctx.value.lower() in crate.CrateName.lower()]
    return None


class ItemSearch(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
    
    search = SlashCommandGroup("search",
                               description = "Commands relating to searching.")
    
    
    @search.command(
        name = "item",
        description = "Search for an item by name.")
    @option("item", description="Pick an item!", autocomplete = itemNameTabComplete)
    async def itemSearchCommand(self,
                          ctx: discord.ApplicationContext,
                          item: str):
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        itemNameList = [x.ItemName for x in itemsList]
        if item not in itemNameList:
            raise ItemNotInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        itemObject = [x for x in itemsList if x.ItemName == item][0]
        embed = await itemToEmbed(itemObject, crateList)
        await ctx.respond(embed = embed)
        
    
    @search.command(
        name = "tag",
        description = "Search for items with a designated tag.")
    @option("tag", description = "Pick a tag!", autocomplete = tagNameTabComplete)
    async def tagSearchCommand(self,
                               ctx: discord.ApplicationContext,
                               tag: str):
        tagsList = await getTagList()
        if not tagsList:
            raise NoTagsInDatabaseError
        if tag not in tagsList:
            raise TagNotInDatabaseError
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        itemsWithTag = [await itemToEmbed(item, crateList) for item in itemsList if tag in [item.TagPrimary, item.TagSecondary, item.TagTertiary]]
        paginator = buildPaginator(itemsWithTag)
        await paginator.respond(ctx.interaction, ephemeral = False)
        
    @search.command(
        name = "term",
        description = "Search for a word or phrase through the item's lore."
    )
    @option("term", description = "Enter a phrase!", input_type = str)
    async def termSearchCommand(self,
                                ctx: discord.ApplicationContext,
                                term: str):
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        itemsFound = [await itemToEmbed(item, crateList) for item in itemsList if term.lower() in item.ItemHuman.lower()]
        if not itemsFound:
            raise NoResultsFoundError
        
        paginator = buildPaginator(itemsFound)
        await paginator.respond(ctx.interaction, ephemeral = False)
        
    @search.command(
        name = "crate",
        description = "Search by Crate."
    )
    @option("crate", description = "Pick a crate!", autocomplete = crateNameTabComplete)
    async def crateSearchCommand(self,
                                 ctx: discord.ApplicationContext,
                                 crate: str):
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        if crate not in [potCrate.CrateName for potCrate in crateList]:
            raise CrateNotInDatabaseError
        crateID = [potCrate.id for potCrate in crateList if potCrate.CrateName == crate][0]
        itemsFound = [await itemToEmbed(item, crateList) for item in itemsList if item.CrateID == crateID]
        if not itemsFound:
            raise NoResultsFoundError
        paginator = buildPaginator(itemsFound)
        await paginator.respond(ctx.interaction, ephemeral = False)
    
    
    
def setup(bot: discord.Bot):
    bot.add_cog(ItemSearch(bot))