import discord
from discord.ext import pages

import core.db as db
from core.models.Item import Item, dictToItem
from core.models.Crate import Crate, dictToCrate
from core.models.MiscItem import MiscItem, dictToMiscItem
from core.models.MiscGroup import MiscGroup, dictToMiscGroup
from core.env import server_name, webAddress
from PIL import Image
import io
import re
import os, aiohttp
from typing import List, Tuple


symbolsToRemove = [
    "✦", 
    "❂", 
    "■", 
    "☀", 
    "☠", 
    "▲", 
    "❃", 
    "◇", 
    "✿", 
    "♦",
    "❀",
    "♆",
    "๑",
    "⊱",
    "⊰",
    "⋗",
    "⋖",
    "❤",
    "❉",
    "✲",
    "◈"
    ]

def makeFile(item: Item):
    return discord.File(f"img/{server_name}/{item.id}.png", filename = f"{item.id}.png", description = f"{item.ItemName}")

def combineImages(items: List[Item]):
    images = [Image.open(f"img/{server_name}/{item.id}.png") for item in items]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_image = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    for im in images:
        new_image.paste(im, (x_offset, 0))
        x_offset += im.size[0]
        
    with io.BytesIO() as image_binary:
        new_image.save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(image_binary, filename=f"{"_".join([str(item.id) for item in items])}.png", description=f"Comparision of the following items: {", ".join([item.ItemName for item in items])}")

def makeIcon(item: Item):
    path = f"img/{server_name}_Icons/{item.id}.png"
    if os.path.isfile(path):
        return discord.File(path, filename = f"{item.id}_icon.png", description = f"{item.ItemName} Icon")
    else: return None

def buildPaginator(pageList: List[discord.Embed]):
    pagelist = [
        pages.PaginatorButton("first", label="⏪", style=discord.ButtonStyle.green),
        pages.PaginatorButton("prev", label="⬅️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
        pages.PaginatorButton("next", label="➡️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("last", label="⏩", style=discord.ButtonStyle.green)
    ]
    prettyPages = []
    for embed in pageList:
        prettyPages.append(pages.Page(embeds=[embed]))
    inator = pages.Paginator(
                pages = prettyPages, # type: ignore
                show_disabled = True,
                show_indicator = True,
                use_default_buttons = False,
                custom_buttons = pagelist,
                loop_pages = True
            )
    inator.pages
    return inator

def buildPopularityPaginator(pageList: List[discord.Embed]):
    pagelist = [
        pages.PaginatorButton("first", label="⏪", style=discord.ButtonStyle.green),
        pages.PaginatorButton("prev", label="⬅️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
        pages.PaginatorButton("next", label="➡️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("last", label="⏩", style=discord.ButtonStyle.green)
    ]
    prettyPages = []
    for embed in pageList:
            prettyPages.append(pages.Page(embeds=[embed]))
    inator = pages.Paginator(
                pages = prettyPages, # type: ignore
                show_disabled = True,
                show_indicator = True,
                use_default_buttons = False,
                custom_buttons = pagelist,
                loop_pages = True
            )
    inator.pages
    return inator

async def crateIDToCrateName(id: int) -> str | None:
    crateList = await db.getCrateList()
    if crateList:
        return [x for x in crateList if id == x.id][0].CrateName
    return None

async def updateFromSite():
    async with aiohttp.ClientSession() as session:
        # Get Item List
        infoPieces = ["id", "CrateID", "TagPrimary", "TagSecondary", "TagTertiary", "TagQuaternary", "TagQuinary", "TagSenary", "TagSeptenary", "WinPercentage", "RarityHuman", "ItemName", "Notes", "ItemHuman", "ImageType", "ConnectedItems"]
        headers = { "I-INCLUDED-INFO" : ";".join(infoPieces)}
        async with session.get(f"{webAddress}/items", headers = headers) as response:
            itemRes = await response.json()
        items: List[Item] = []
        existingPictures = await db.getImageList()
        missingPictures = []
        if itemRes["data"]:
            for item in itemRes["data"]:
                item = dictToItem(item)
                if item.id in existingPictures:
                    items.append(item)
                else:
                    async with session.get(f"{webAddress.replace("/api", "")}/static/images/{server_name}_Descriptions/{item.id}.png") as response: # type: ignore
                        content_type = response.headers.get("Content-Type", "").lower()
                        if content_type.startswith("image/"):
                            existingPictures.append(item.id)
                            items.append(item)
                        else:
                            missingPictures.append(item)
        await db.updateImageList(existingPictures)
        await db.updateItemList(items)
        # Get Crate List
        async with session.get(f"{webAddress}/crates") as response:
            crateRes = await response.json()
        crates: List[Crate] = []
        if crateRes:
            crates = [dictToCrate(x) for x in crateRes]
        await db.updateCrateList(crates)
        # Get Tag List
        async with session.get(f"{webAddress}/tags") as response:
            tagRes = await response.json()
        tags = []
        if tagRes:
            tags = tagRes
        await db.updateTagList(tagRes)
        
        # Get Misc Item List
        infoPieces = ["id", "GroupID", "ItemName", "Notes", "ItemHuman", "ImageType"]
        headers = { "I-INCLUDED-INFO" : ";".join(infoPieces)}
        async with session.get(f"{webAddress}/miscitems", headers = headers) as response:
            itemRes = await response.json()
        miscItems: List[MiscItem] = []
        existingPictures = await db.getMiscImageList()
        missingMiscPictures = []
        if itemRes["data"]:
            for item in itemRes["data"]:
                item = dictToMiscItem(item)
                if item.id in existingPictures:
                    miscItems.append(item)
                else:
                    async with session.get(f"{webAddress.replace("/api", "")}/static/images/{server_name}_Misc_Descriptions/{item.id}.png") as response: # type: ignore
                        content_type = response.headers.get("Content-Type", "").lower()
                        if content_type.startswith("image/"):
                            existingPictures.append(item.id)
                            miscItems.append(item)
                        else:
                            missingMiscPictures.append(item)
        await db.updateMiscImageList(existingPictures)
        await db.updateMiscItemList(miscItems)
        # Get Group List
        async with session.get(f"{webAddress}/miscgroups") as response:
            crateRes = await response.json()
        groups: List[MiscGroup] = []
        if crateRes:
            groups = [dictToMiscGroup(x) for x in crateRes]
        await db.updateGroupList(groups)
        
    return missingPictures, missingMiscPictures
        
def roman_to_int(numeral: str):
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    # Additive approach: check if current is smaller than next, if so, subtract
    for i in range(len(numeral)):
        if i + 1 < len(numeral) and roman_map[numeral[i]] < roman_map[numeral[i+1]]:
            total -= roman_map[numeral[i]]
        else:
            total += roman_map[numeral[i]]
    return total

def convert_roman_in_string(text: str):
    # Matches roman numerals (I,V,X,L,C,D,M) only if they are separate words
    pattern = r'\b[IVXLCDM]+\b'
    
    def replacer(match):
        return str(roman_to_int(match.group(0)))
    
    return re.sub(pattern, replacer, text)

def convert_int_to_roman(text: str):
    newText = text
    map = {
        10 : "X",
        9 : "IX",
        8 : "VIII",
        7 : "VII",
        6 : "VI",
        5 : "V",
        4 : "IV",
        3 : "III",
        2 : "II",
        1 : "I"
    }
    for num, roman in map.items():
        newText = newText.replace(str(num), roman)
    return newText