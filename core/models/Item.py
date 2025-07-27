from dataclasses import dataclass
from typing import Dict, List
import discord




from core.env import itemImageAddress, itemSoloAddress
from core.models.Crate import Crate

@dataclass
class Item:
    """Helper class to standardize Items
    """
    id: int
    
    CrateID: int
    TagPrimary: str
    TagSecondary: str
    TagTertiary: str
    WinPercentage: str
    RarityHuman: str
    ItemName: str    
    Notes: str
    ItemHuman: str

def dictToItem(item: Dict[str, str]):
    return Item(
            int(item["id"]),
            int(item["CrateID"]),
            item["TagPrimary"],
            item["TagSecondary"],
            item["TagTertiary"],
            item["WinPercentage"],
            item["RarityHuman"],
            item["ItemName"],
            item["Notes"],
            item["ItemHuman"]
            )



async def itemToEmbed(item: Item, crateList: List[Crate]) -> discord.Embed:
    embed = discord.Embed(title = f"{item.ItemName}",
                      url=f"{itemSoloAddress}/{item.id}",
                      colour=0x00b0f4)
    if item.CrateID:
        crateName = [x for x in crateList if item.CrateID == x.id][0].CrateName
        embed.add_field(name = "Crate Name",
                        value = f"{crateName}",
                        inline = True)
    if item.TagPrimary:
        embed.add_field(name = "Primary Tag",
                        value = f"{item.TagPrimary}",
                        inline = True)
    if item.TagSecondary:
        embed.add_field(name = "Secondary Tag",
                        value = f"{item.TagSecondary}",
                        inline = True)
    if item.TagTertiary:
        embed.add_field(name = "Tertiary Tag",
                        value = f"{item.TagTertiary}",
                        inline = True)
    if item.WinPercentage:
        embed.add_field(name = "Win Percentage",
                        value = f"{item.WinPercentage}",
                        inline = True)
    if item.RarityHuman:
        embed.add_field(name = "Rarity",
                        value = f"{item.RarityHuman}",
                        inline = True)
    if item.Notes:
        embed.add_field(name = "Notes",
                        value = f"{item.Notes}",
                        inline = False)

    embed.set_image(url=f"{itemImageAddress}/{item.id}.png")
    return embed