import discord
from discord.ext import commands
from discord.commands import option, SlashCommandGroup
from typing import List
from core.db import getItemListTabComplete, getItemList, getCrateList
import core.vault_db as vault
from core.models.VaultEntry import VaultEntry
from core.cogs.ErrorDefinitions import *





servers = ["Arcane", "Cosmic", "Elysium"]
#                         Alex                 aari                  yofun               linoha
validUsers = [899005507514302524, 889213585690067065, 288157206585671681, 1253252589240324158]

def checkUser(ctx: discord.ApplicationContext):
    return ctx.author.id in validUsers

async def itemNameTabComplete(ctx: discord.AutocompleteContext):
    itemsList = await getItemListTabComplete()
    if itemsList:
        return [item for item in itemsList if ctx.value.lower() in item.lower()]
    return None

async def vaultToEmbed(currentVault: List[VaultEntry], itemName: str) -> discord.Embed:
    actualItems = [x for x in currentVault if x.ItemName == itemName]
    embed = discord.Embed(title=f"{itemName}",
                          description="```\nFormat:\nid - Donator\n```",
                          colour=0x00b0f4)
    for server in servers:
        serverValue = "```\n"
        serverItems = [x for x in actualItems if x.Server == server]
        if serverItems:
            for entry in serverItems:
                serverValue += f"{entry.id} - {entry.Donor}\n"
        else:
            serverValue += "No donations, yet.\n"
        embed.add_field(name = f"{server} ({len(serverItems)})", value = f"{serverValue}```", inline = False)
    return embed

async def vaultToDonorEmbed(currentVault: List[VaultEntry], donor: str) -> discord.Embed:
    actualItems = [x for x in currentVault if x.Donor == donor]
    embed = discord.Embed(title=f"{donor}",
                          description="```\nFormat:\nid - Item\n```",
                          colour=0x00b0f4)
    for server in servers:
        serverValue = "```\n"
        serverItems = [x for x in actualItems if x.Server == server]
        if serverItems:
            for entry in serverItems:
                serverValue += f"{entry.id} - {entry.ItemName}\n"
        else:
            serverValue += "No donations, yet.\n"
        embed.add_field(name = f"{server} ({len(serverItems)})", value = f"{serverValue}```", inline = False)
    return embed

class Vault(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
    
    vault = SlashCommandGroup("vault",
                               description = "Commands related to the Vault.")
    
    
    @vault.command(
        name = "addentry",
        description = "Add an item to the Vault")
    @option("item", description="Pick an item!", autocomplete = itemNameTabComplete, required = True)
    @option("server", description = "Which server is the item on?", choices = ["Arcane", "Cosmic", "Elysium"], required = True)
    @option("donor", description="Who donated the item?", required = False, default = "")
    @commands.check(checkUser) # type: ignore
    async def vaultAddEntryCommand(self,
                          ctx: discord.ApplicationContext,
                          item: str,
                          server: str,
                          donor: str):
        if donor == "": donor = None # type: ignore
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
        crateName = [x for x in crateList if itemObject.CrateID == x.id][0].CrateName
        
        entry = VaultEntry(await vault.getNextID(), itemObject.ItemName, crateName, donor, server)
        res = await vault.addEntry(entry)
        if res: 
            await ctx.respond(f"Entry added with id: {entry.id}")
        else:
            await ctx.respond("Something went wrong :(")
    
    @vault.command(
        name = "viewitem",
        description = "View inventory info on an item.")
    @option("item", description="Pick an item!", autocomplete = itemNameTabComplete, required = True)
    async def vaultViewItemCommand(self,
                          ctx: discord.ApplicationContext,
                          item: str):
        currentVault = await vault.getVault()
        if currentVault:
            embed = await vaultToEmbed(currentVault, item)
            await ctx.respond(embed = embed)
        else:
            await ctx.respond("No items in vault whatsoever :(")
            
    @vault.command(
        name = "deleteentry",
        description = "Remove a donation from the database.")
    @option("id", description="Enter the entry ID!", required = True)
    @commands.check(checkUser) # type: ignore
    async def vaultDeleteEntryCommand(self,
                          ctx: discord.ApplicationContext,
                          id: int):
        if await vault.deleteEntry(id):
            await ctx.respond(f"Entry ID: {id} Deleted.")
        else:
            await ctx.respond("Something happened.")
    
    @vault.command(
        name = "lookupdonor",
        description = "Look at all donations from an individual.")
    @option("donor", description="Enter the name of the Donor.", required = True)
    async def vaultViewDonorCommand(self,
                          ctx: discord.ApplicationContext,
                          donor: str):
        if donor == "None": donor = None # type: ignore
        currentVault = await vault.getVault()
        if currentVault:
            embed = await vaultToDonorEmbed(currentVault, donor)
            await ctx.respond(embed = embed)
        else:
            await ctx.respond("No items in vault whatsoever :(")


def setup(bot: discord.Bot):
    bot.add_cog(Vault(bot))