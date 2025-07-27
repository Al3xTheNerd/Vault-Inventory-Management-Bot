from dataclasses import dataclass
from typing import Dict
@dataclass
class Crate:
    """Helper class to standardize Items
    """
    id: int
    
    CrateName: str
    ReleaseDate: str
    URLTag: str


def dictToCrate(crate: Dict[str, str]):
    return Crate(
            int(crate["id"]),
            crate["CrateName"],
            crate["ReleaseDate"],
            crate["URLTag"],
            )