import discord, aiohttp, random
from discord.ext import commands, tasks
from typing import List


import core.db as db
from core.env import webAddress
from core.models.Item import Item, dictToItem
from core.models.Crate import Crate, dictToCrate
from core.utils import symbolsToRemove, updateFromSite



class RepeatingTasksCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.pullData.start()


    @tasks.loop(minutes=30)
    async def pullData(self):
        print("Refreshing Data.")
        await updateFromSite()
        
def setup(bot: discord.Bot):
    bot.add_cog(RepeatingTasksCog(bot))