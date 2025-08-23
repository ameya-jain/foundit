
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class VectorSearchService(ABC):
    @abstractmethod
    async def insert_item_vector(self, item_id: str, vector: List[float], payload: Dict) -> None:
        """
        Insert an item vector with associated metadata payload.
        """
        pass

    @abstractmethod
    async def search_similar(self, vector: List[float], top_k: int = 5, filter_payload: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar vectors and return top-K matches with their metadata.
        """
        pass
