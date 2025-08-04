from core.env import vaultDatabaseFile
from core.models.VaultEntry import VaultEntry, dictToVaultEntry
from typing import List, Dict
from pickledb import AsyncPickleDB
if not vaultDatabaseFile: raise


async def getVault() -> List[VaultEntry] | None:
    try:
        with AsyncPickleDB(vaultDatabaseFile) as database:
            correctEntries = None
            entries: List[Dict[str, str]] | None = await database.aget("vault")
            if entries:
                correctEntries: List[VaultEntry] | None = [dictToVaultEntry(x) for x in entries]
        return correctEntries
    except:
        return None
    
async def vaultItemNameTabComplete() -> List[VaultEntry] | None:
    try:
        with AsyncPickleDB(vaultDatabaseFile) as database:
            correctItems = None
            items: List[Dict[str, str]] | None = await database.aget("vault")
            if items:
                correctItems: List[str] | None = [dictToVaultEntry(x).ItemName for x in items]
        return correctItems # type: ignore
    except:
        return None

async def updateVault(entries: List[VaultEntry]) -> bool:
    try:
        with AsyncPickleDB(vaultDatabaseFile) as database:
            await database.aset("vault", entries)
        return True
    except:
        return False

async def addEntry(entry: VaultEntry) -> bool:
    currentVault = await getVault()
    if currentVault:
        currentVault.append(entry)
    else:
        currentVault = [entry]
    res = await updateVault(currentVault)
    return res

async def deleteEntry(id: int) -> bool:
    currentVault = await getVault()
    if currentVault:
        newVault = [entry for entry in currentVault if entry.id != id]
    else:
        newVault = []
    res = await updateVault(newVault)
    return res

async def getNextID() -> int:
    currentVault = await getVault()
    if currentVault:
        validNum = False
        potentialNum = len(currentVault) + 1
        while validNum == False:
            if checkID(potentialNum, currentVault):
                validNum = True
            else:
                potentialNum += 1
        return potentialNum
    return 1
        

def checkID(potential: int, currentVault: List[VaultEntry]) -> bool:
    validityCheck = [num.id for num in currentVault if num.id == potential]
    if len(validityCheck) > 0:
        return False
    return True