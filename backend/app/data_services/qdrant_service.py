from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from app.data_services.base.vector_interface import VectorSearchService
from app.config.settings import settings
from typing import List, Dict, Optional

class QdrantVectorService(VectorSearchService):
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
        self.collection = settings.QDRANT_COLLECTION

    async def insert_item_vector(self, item_id: str, vector: List[float], payload: Dict) -> None:
        point = PointStruct(id=item_id, vector=vector, payload=payload)
        self.client.upsert(collection_name=self.collection, points=[point])

    async def search_similar(self, vector: List[float], top_k: int = 5, filter_payload: Optional[Dict] = None) -> List[Dict]:
        filter = None
        if filter_payload:
            conditions = [
                FieldCondition(key=key, match=MatchValue(value=val))
                for key, val in filter_payload.items()
            ]
            filter = Filter(must=conditions)

        hits = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=top_k,
            query_filter=filter
        )

        return [
            {
                "id": str(hit.id),
                "score": hit.score,
                "payload": hit.payload
            }
            for hit in hits
        ]
