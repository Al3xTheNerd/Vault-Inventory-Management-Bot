import discord
from discord.ext import commands
from discord.commands import option, SlashCommandGroup

from core.db import getItemListTabComplete, getItemList, getCrateList, getTagList, addOneToItemCounter, getItemCounter
from core.db import getMiscItemList, getGroupList, getMiscItemListTabComplete
from core.models.Item import itemToEmbed, Item
from core.models.MiscItem import miscItemToEmbed, MiscItem
from core.cogs.ErrorDefinitions import *
from core.utils import buildPaginator, combineImages, convert_roman_in_string, convert_int_to_roman

from typing import List

async def itemNameTabComplete(ctx: discord.AutocompleteContext):
    itemsList = await getItemListTabComplete()
    itemCounts = await getItemCounter()
    returnInfo = []
    if itemsList:
        if itemCounts:
            if ctx.value == "":
                mostPopular = list(dict(sorted(itemCounts.items(), key=lambda item: item[1])).keys())
                mostPopular.reverse()
                returnInfo += [x for x in mostPopular]
                returnInfo += [x for x in itemsList if x not in returnInfo]
                return returnInfo
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

async def groupNameTabComplete(ctx: discord.AutocompleteContext):
    groupList = await getGroupList()
    if groupList:
        return [group.GroupName for group in groupList if ctx.value.lower() in group.GroupName.lower()]
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
        groupList = await getGroupList()
        itemObject = [x for x in itemsList if x.ItemName == item][0]
        timesRequested = await addOneToItemCounter(item)
        embed = await itemToEmbed(itemObject, crateList, timesRequested, groupList)
        if embed and embed.image:
            print(embed.image.url)
        await ctx.respond(embed = embed)

    @search.command(
        name = "compare",
        description = "Compare two or more items!")
    @option("item", description="Pick an item!", autocomplete = itemNameTabComplete, required=True)
    @option("item_two", description = "Pick another item!", autocomplete = itemNameTabComplete, required=True, default="")
    @option("item_three", description = "Pick another item!", autocomplete = itemNameTabComplete, required=False, default="")
    @option("item_four", description = "Pick another item!", autocomplete = itemNameTabComplete, required=False, default="")
    @option("item_five", description = "Pick another item!", autocomplete = itemNameTabComplete, required=False, default="")
    @option("item_six", description = "Pick another item!", autocomplete = itemNameTabComplete, required=False, default="")
    @option("item_seven", description = "Pick another item!", autocomplete = itemNameTabComplete, required=False, default="")
    @option("item_eight", description = "Pick another item!", autocomplete = itemNameTabComplete, required=False, default="")
    @option("item_nine", description = "Pick another item!", autocomplete = itemNameTabComplete, required=False, default="")
    @option("item_ten", description = "Pick another item!", autocomplete = itemNameTabComplete, required=False, default="")
    async def itemCombineCommand(self,
                          ctx: discord.ApplicationContext,
                          item: str,
                          item_two: str,
                          item_three: str,
                          item_four: str,
                          item_five: str,
                          item_six: str,
                          item_seven: str,
                          item_eight: str,
                          item_nine: str,
                          item_ten: str):
        comparisonItems = [x for x in [item, item_two, item_three, item_four, item_five, item_six, item_seven, item_eight, item_nine, item_ten] if x != ""]
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        itemNameList = [x.ItemName for x in itemsList]
        if item not in itemNameList:
            raise ItemNotInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        
        comparisonObjects: List[Item] = []
        for itemName in comparisonItems:
            comparisonObjects.append([x for x in itemsList if x.ItemName == itemName][0])
        combinationImage = combineImages(comparisonObjects)
        responseMessage = "Here is your comparison of the following items:"
        for each in comparisonObjects:
            responseMessage += f"\n- {each.ItemName}"
        await ctx.respond(responseMessage, file=combinationImage)
        
    
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
        groupList = await getGroupList()
        itemsWithTag = [(await itemToEmbed(item, crateList, await addOneToItemCounter(item.ItemName), groupList)) for item in itemsList if tag in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSenary, item.TagSeptenary] and "Repeat Appearance" not in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSenary, item.TagSeptenary]]

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
        groupList = await getGroupList()
        itemsFound = []
        for item in itemsList:
            loweredItemHuman = item.ItemHuman.lower()
            if term.lower() in loweredItemHuman or convert_roman_in_string(term).lower() in loweredItemHuman or convert_int_to_roman(term).lower() in loweredItemHuman:
                if "Repeat Appearance" not in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSenary, item.TagSeptenary]:
                    itemsFound.append((await itemToEmbed(item, crateList, await addOneToItemCounter(item.ItemName), groupList)))
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
        await ctx.defer()
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        if crate not in [potCrate.CrateName for potCrate in crateList]:
            raise CrateNotInDatabaseError
        groupList = await getGroupList()
        crateID = [potCrate.id for potCrate in crateList if potCrate.CrateName == crate][0]
        itemsFound = [(await itemToEmbed(item, crateList, await addOneToItemCounter(item.ItemName), groupList)) for item in itemsList if item.CrateID == crateID]
        if not itemsFound:
            raise NoResultsFoundError
        paginator = buildPaginator(itemsFound)
        await paginator.respond(ctx.interaction, ephemeral = False)
    
    @search.command(
        name = "group",
        description = "Search by Miscellanous Group."
    )
    @option("group", description = "Pick a group!", autocomplete = groupNameTabComplete)
    async def groupSearchCommand(self,
                                 ctx: discord.ApplicationContext,
                                 group: str):
        itemsList = await getMiscItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getGroupList()
        if not crateList:
            raise NoCratesInDatabaseError
        if group not in [potCrate.GroupName for potCrate in crateList]:
            raise CrateNotInDatabaseError
        crateID = [potCrate.id for potCrate in crateList if potCrate.GroupName == group][0]
        itemsFound = [(await miscItemToEmbed(item, crateList, None)) for item in itemsList if item.GroupID == crateID]
        if not itemsFound:
            raise NoResultsFoundError
        paginator = buildPaginator(itemsFound)
        await paginator.respond(ctx.interaction, ephemeral = False)


    @search.command(
        name = "advanced",
        description = "Search by multiple constraints."
    )
    @option("crate", description = "Pick a crate!", autocomplete = crateNameTabComplete, required=False, default="")
    @option("term", description = "Enter a phrase!", required=False, default="", input_type=str)
    @option("tag", description = "Pick a tag!", autocomplete = tagNameTabComplete, required=False, default="", input_type=str)
    async def advancedSearchCommand(self,
                                 ctx: discord.ApplicationContext,
                                 crate: str,
                                 term: str,
                                 tag: str):
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        groupList = await getGroupList()
        if crate == "" and term == "" and tag == "":
            raise MinimumConstraintError
        
        if crate != "":
            if crate not in [potCrate.CrateName for potCrate in crateList]:
                raise CrateNotInDatabaseError
            crateID = [potCrate.id for potCrate in crateList if potCrate.CrateName == crate][0]

        if tag != "":
            tagsList = await getTagList()
            if not tagsList:
                raise NoTagsInDatabaseError
            if tag not in tagsList:
                raise TagNotInDatabaseError
            

        
        sortedItems = []
        for item in itemsList:
            meetsAllConditions = False
            itemTags = [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSenary, item.TagSeptenary]
            if "Repeat Appearance" in itemTags:
                continue
            if crate != "":
                if item.CrateID != crateID: # type: ignore
                    continue
            if tag != "":
                if tag not in itemTags:
                    continue
            if term != "":
                loweredItemHuman = item.ItemHuman.lower()
                if term.lower() not in loweredItemHuman and convert_roman_in_string(term).lower() not in loweredItemHuman and convert_int_to_roman(term).lower() not in loweredItemHuman:
                    continue
            embedPage = await itemToEmbed(item, crateList, await addOneToItemCounter(item.ItemName), groupList)
            sortedItems.append(embedPage)
        
        
        if not sortedItems:
            raise NoResultsFoundError
        paginator = buildPaginator(sortedItems)
        await paginator.respond(ctx.interaction, ephemeral = False)
    
def setup(bot: discord.Bot):
    bot.add_cog(ItemSearch(bot))