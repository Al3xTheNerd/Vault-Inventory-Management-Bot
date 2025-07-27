import discord
from discord.ext import pages
from typing import List

from core.db import getCrateList






def buildPaginator(pageList: List[discord.Embed]):
    pagelist = [
        pages.PaginatorButton("first", label="⏪", style=discord.ButtonStyle.green),
        pages.PaginatorButton("prev", label="⬅️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
        pages.PaginatorButton("next", label="➡️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("last", label="⏩", style=discord.ButtonStyle.green)
    ]
    inator = pages.Paginator(
                pages = pageList, # type: ignore
                show_disabled = True,
                show_indicator = True,
                use_default_buttons = False,
                custom_buttons = pagelist,
                loop_pages = True
            )
    return inator

async def crateIDToCrateName(id: int) -> str | None:
    crateList = await getCrateList()
    if crateList:
        return [x for x in crateList if id == x.id][0].CrateName
    return None

