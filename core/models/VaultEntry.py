from dataclasses import dataclass
from typing import Dict


@dataclass
class VaultEntry:
    """Helper class to standardize Vault Entries"""
    id: int
    ItemName: str
    CrateName: str
    Donor: str |  None
    Server: str

def dictToVaultEntry(entry: Dict[str, str]):
    return VaultEntry(
            int(entry["id"]),
            entry["ItemName"],
            entry["CrateName"],
            entry["Donor"],
            entry["Server"]
            )

