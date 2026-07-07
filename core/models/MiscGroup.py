from dataclasses import dataclass
from typing import Dict
@dataclass
class MiscGroup:
    """Helper class to standardize Miscellaneous Groups
    """
    id: int
    
    GroupName: str
    ReleaseDate: str
    URLTag: str
    GroupType: str
    Notes: str


def dictToMiscGroup(group: Dict[str, str]):
    return MiscGroup(
            int(group["id"]),
            group["GroupName"],
            group["ReleaseDate"],
            group["URLTag"],
            group["GroupType"],
            group["Notes"]
            )