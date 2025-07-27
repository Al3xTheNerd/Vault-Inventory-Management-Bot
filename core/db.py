from typing import Dict, List
from pickledb import AsyncPickleDB


from core.env import databaseFile
from core.models.Item import Item, dictToItem
from core.models.Crate import Crate, dictToCrate


async def updateItemList(items: List[Item]) -> bool:
    """Updates the full item list in db.
    Args:
        items (List[Item]): A list of Item Objects.
    Returns:
        bool: True if no errors occur, False if something fucks up."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            await database.aset("items", items)
        return True
    except:
        return False

async def getItemList() -> List[Item] | None:
    """Returns the full item list.
    Returns:
        List[Item] | None: Returns full item list, or None if no items are saved."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            correctItems = None
            items: List[Dict[str, str]] | None = await database.aget("items")
            if items:
                correctItems: List[Item] | None = [dictToItem(x) for x in items]
        return correctItems
    except:
        return None
    
async def getItemListTabComplete() -> List[str] | None:
    """Returns the full item list.
    Returns:
        List[Item] | None: Returns full item list, or None if no items are saved."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            correctItems = None
            items: List[Dict[str, str]] | None = await database.aget("items")
            if items:
                correctItems: List[str] | None = [dictToItem(x).ItemName for x in items]
        return correctItems
    except:
        return None
    


async def updateCrateList(crates: List[Crate]) -> bool:
    """Updates the full crate list in db.
    Args:
        items (List[Crate]): A list of Item Objects.
    Returns:
        bool: True if no errors occur, False if something fucks up."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            await database.aset("crates", crates)
        return True
    except:
        return False

async def getCrateList() -> List[Crate] | None:
    """Returns the full crate list.
    Returns:
        List[Crate] | None: Returns full crate list, or None if no items are saved."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            correctCrates = None
            crates: List[Dict[str, str]] | None = await database.aget("crates")
            if crates:
                correctCrates: List[Crate] | None = [dictToCrate(x) for x in crates]
        return correctCrates
    except:
        return None


async def updateTagList(tags: List[str]) -> bool:
    """Updates the full tag list in db.
    Args:
        items (List[str]): A list of Tags.
    Returns:
        bool: True if no errors occur, False if something fucks up."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            await database.aset("tags", tags)
        return True
    except:
        return False

async def getTagList() -> List[str] | None:
    """Returns the full tag list.
    Returns:
        List[str] | None: Returns full tag list, or None if no tags are saved."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            return await database.aget("tags")
    except:
        return None