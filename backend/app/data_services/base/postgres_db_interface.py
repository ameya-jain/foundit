from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class ItemRepository(ABC):
    @abstractmethod
    async def insert_found_item(self, item_data: Dict) -> str:
        """
        Insert found item metadata into Postgres and return the new item ID (UUID).
        """
        pass

    @abstractmethod
    async def get_found_item_by_id(self, item_id: str) -> Optional[Dict]:
        """
        Fetch found item metadata from Postgres by ID.
        """
        pass

    @abstractmethod
    async def insert_lost_report(self, report_data: Dict) -> str:
        """
        Insert lost report metadata into Postgres and return the new report ID (UUID).
        """
        pass

    @abstractmethod
    async def get_lost_report_by_id(self, report_id: str) -> Optional[Dict]:
        """
        Fetch lost report metadata from Postgres by ID.
        """
        pass

    @abstractmethod
    async def insert_matches(self, matches: List[Dict]) -> None:
        """
        Insert match results into the matches table.
        Each dict contains: found_item_id, lost_item_id, score
        """
        pass