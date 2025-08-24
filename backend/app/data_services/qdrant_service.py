from typing import List, Dict, Optional
import logging
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue, Condition
from app.config.settings import settings
from app.infra.qdrant_client import qdrant_client
from app.data_services.base.vector_interface import VectorSearchService

logger = logging.getLogger(__name__)


class QdrantVectorService(VectorSearchService):
    def __init__(self, collection: str = settings.QDRANT_COLLECTION):
        self.client = qdrant_client.get_client()
        self.collection = collection

    async def insert_item_vector(self, item_id: int, vector: List[float], payload: Dict) -> None:
        try:
            point = PointStruct(id=item_id, vector=vector, payload=payload)
            await self.client.upsert(collection_name=self.collection, points=[point])
        except Exception as e:
            logger.error(f"Failed to upsert vector {item_id}: {e}")
            raise

    async def search_similar(
        self, vector: List[float], top_k: int = 5, filter_payload: Optional[Dict] = None
    ) -> List[Dict]:
        try:
            query_filter = None
            if filter_payload:
                conditions: List[Condition] = [
                    FieldCondition(key=k, match=MatchValue(value=v))
                    for k, v in filter_payload.items()
                ]
                query_filter = Filter(must=conditions)

            hits = await self.client.search(
                collection_name=self.collection,
                query_vector=vector,
                limit=top_k,
                query_filter=query_filter,
            )

            return [{"id": str(hit.id), "score": hit.score, "payload": hit.payload} for hit in hits]
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
