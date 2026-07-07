from dataclasses import dataclass
from typing import Dict, List
import discord
import os




from core.env import itemImageAddress, itemSoloAddress
from core.models.MiscGroup import MiscGroup

@dataclass
class MiscItem:
    """Helper class to standardize Miscellaneous Items
    """
    id: int
    
    GroupID: int
    ItemName: str
    Notes: str
    ItemHuman: str
    ImageType: str

def dictToMiscItem(item: Dict[str, str]):
    return MiscItem(
            int(item["id"]),
            int(item["GroupID"]),
            item["ItemName"],
            item["Notes"],
            item["ItemHuman"],
            item["ImageType"]
            ) # type: ignore


async def miscItemToEmbed(item: MiscItem, groupList: List[MiscGroup], timesSeen: int | None) -> discord.Embed:
    group = [x for x in groupList if item.GroupID == x.id][0]
    embed = discord.Embed(title = f"{group.GroupName}",
                      url=f"{itemSoloAddress.replace("item", "group")}/{group.URLTag}", # type: ignore
                      colour=0x00b0f4)
    
    embed.add_field(name = "Item",
                    value = f"{item.ItemName}",
                    inline = False)
    if group.ReleaseDate:
        embed.add_field(name = "Group Release Date",
                        value = f"{group.ReleaseDate}",
                        inline = False)
    if group.Notes:
        embed.add_field(name = "Group Notes",
                        value = f"{group.Notes}",
                        inline = False)
    if item.Notes:
        embed.add_field(name = "Item Notes",
                        value = f"{item.Notes}",
                        inline = False)

    embed.set_image(url=f"{itemImageAddress.replace("Icons", "Misc_Descriptions")}/{item.id}.png") # type: ignore
    embed.set_thumbnail(url=f"{itemImageAddress.replace("Icons", "Misc_Icons")}/{item.id}.{item.ImageType}") # type: ignore
    if timesSeen:
        embed.set_footer(text=f"Times Searched: {timesSeen}")
    return embed