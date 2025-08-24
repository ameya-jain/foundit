import logging
from app.ml_services.base import ImageProcessingService, TextEmbeddingService
from app.ml_services.openai_service import OpenAIImageService, OpenAITextService

from app.data_services.base.postgres_db_interface import ItemRepository
from app.data_services.base.storage_interface import ImageStorageService
from app.data_services.base.vector_interface import VectorSearchService

from app.data_services.postgres_db import PostgresRepository
from app.data_services.supabase_storage import SupabaseStorageService
from app.data_services.qdrant_service import QdrantVectorService

from app.infra.database import db
from app.infra.supabase_client import supabase_client
from app.infra.qdrant_client import qdrant_client
from app.infra.openai_client import openai_client

logger = logging.getLogger(__name__)

class Services:
    def __init__(self):
        self._image_service = None
        self._text_service = None
        self._db_service = None
        self._storage_service = None
        self._vector_service = None

    async def start(self):
        try:
            await db.init()
            supabase_client.init()
            await qdrant_client.init()
            await openai_client.init()
        except Exception as e:
            logger.error(f"Failed to initialize services: {e}")
            raise
    
    async def stop(self):
        await db.close()
        supabase_client.close()
        await qdrant_client.close()
        await openai_client.close()

    @property
    def image_service(self) -> ImageProcessingService:
        if self._image_service is None:
            self._image_service = OpenAIImageService()
        return self._image_service
    
    @property
    def text_service(self) -> TextEmbeddingService:
        if self._text_service is None:
            self._text_service = OpenAITextService()
        return self._text_service
    
    @property
    def db_service(self) -> ItemRepository:
        if self._db_service is None:
            if not db:
                raise RuntimeError("Database not initialized. Call await services.start() first.")
            self._db_service = PostgresRepository(db)
        return self._db_service
    
    @property
    def storage_service(self) -> ImageStorageService:
        if self._storage_service is None:
            self._storage_service = SupabaseStorageService()
        return self._storage_service
    
    @property
    def vector_service(self) -> VectorSearchService:
        if self._vector_service is None:
            self._vector_service = QdrantVectorService()
        return self._vector_service


# Singleton instance
services = Services()

# FastAPI dependency function
def get_services() -> Services:
    return services
