from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class ItemRepository(ABC):
    @abstractmethod
    async def insert_item(self, item_data: Dict) -> str:
        """
        Insert item metadata into Postgres and return the new item ID (UUID).
        """
        pass

    @abstractmethod
    async def insert_matches(self, matches: List[Dict]) -> None:
        """
        Insert match results into the matches table.
        Each dict contains: found_item_id, lost_item_id, score
        """
        pass

    @abstractmethod
    async def get_item_by_id(self, item_id: str) -> Optional[Dict]:
        """
        Optional helper to fetch item metadata by ID.
        """
        pass
