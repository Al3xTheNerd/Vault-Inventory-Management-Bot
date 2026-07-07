from typing import Dict, List
from pickledb import AsyncPickleDB


from core.env import databaseFile
from core.models.Item import Item, dictToItem
from core.models.Crate import Crate, dictToCrate
from core.models.MiscItem import MiscItem, dictToMiscItem
from core.models.MiscGroup import MiscGroup, dictToMiscGroup


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

async def updateMiscItemList(items: List[MiscItem]) -> bool:
    """Updates the full item list in db.
    Args:
        items (List[MiscItem]): A list of Item Objects.
    Returns:
        bool: True if no errors occur, False if something fucks up."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            await database.aset("miscitems", items)
        return True
    except:
        return False

async def getMiscItemList() -> List[MiscItem] | None:
    """Returns the full item list.
    Returns:
        List[MiscItem] | None: Returns full item list, or None if no items are saved."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            correctItems = None
            items: List[Dict[str, str]] | None = await database.aget("miscitems")
            if items:
                correctItems: List[MiscItem] | None = [dictToMiscItem(x) for x in items]
        return correctItems
    except:
        return None

async def getMiscItemListTabComplete() -> List[str] | None:
    """Returns the full item list.
    Returns:
        List[Item] | None: Returns full item list, or None if no items are saved."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            correctItems = None
            items: List[Dict[str, str]] | None = await database.aget("miscitems")
            if items:
                correctItems: List[str] | None = [dictToMiscItem(x).ItemName for x in items]
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

async def updateGroupList(groups: List[MiscGroup]) -> bool:
    """Updates the full crate list in db.
    Args:
        items (List[Crate]): A list of Item Objects.
    Returns:
        bool: True if no errors occur, False if something fucks up."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            await database.aset("groups", groups)
        return True
    except:
        return False

async def getGroupList() -> List[MiscGroup] | None:
    """Returns the full crate list.
    Returns:
        List[Crate] | None: Returns full crate list, or None if no items are saved."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            correctGroups = None
            groups: List[Dict[str, str]] | None = await database.aget("groups")
            if groups:
                correctGroups: List[MiscGroup] | None = [dictToMiscGroup(x) for x in groups]
        return correctGroups
    except:
        return None

async def updateImageList(images: List[int]) -> bool:
    """Updates the full list of existing images in db.
    Args:
        items (List[int]): A list of Item Objects.
    Returns:
        bool: True if no errors occur, False if something fucks up."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            await database.aset("images", images)
        return True
    except Exception as E:
        raise E
        return False

async def getImageList() -> List[int]:
    """Returns the full list of existing images.
    Returns:
        List[int] | None: Returns full image list, or None if no images exist."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            images = await database.aget("images")
            if not images:
                return []
        return images
    except:
        return []


async def updateMiscImageList(images: List[int]) -> bool:
    """Updates the full list of existing images in db.
    Args:
        items (List[int]): A list of Item Objects.
    Returns:
        bool: True if no errors occur, False if something fucks up."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            await database.aset("miscimages", images)
        return True
    except Exception as E:
        raise E
        return False

async def getMiscImageList() -> List[int]:
    """Returns the full list of existing images.
    Returns:
        List[int] | None: Returns full image list, or None if no images exist."""
    try:
        with AsyncPickleDB(databaseFile) as database:
            images = await database.aget("miscimages")
            if not images:
                return []
        return images
    except:
        return []



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

async def addOneToItemCounter(item: str) -> int | bool:
    try:
        with AsyncPickleDB(databaseFile) as database:
            currentCounts: Dict[str, int] | None = await database.aget("itemCounter")
            if not currentCounts:
                currentCounts = {item : 1}
            else:
                if item in currentCounts:
                    currentCounts[item] += 1
                else:
                    currentCounts[item] = 1
            await database.aset("itemCounter", currentCounts)
        return currentCounts[item] # int
    except:
        return False

async def getItemCounter() -> Dict[str, int] | None:
    try:
        with AsyncPickleDB(databaseFile) as database:
            return await database.aget("itemCounter")
    except:
        return None
