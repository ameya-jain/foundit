import logging
from typing import Optional
from qdrant_client.async_qdrant_client import AsyncQdrantClient
from app.config.settings import settings

logger = logging.getLogger(__name__)


class QdrantClient:
    _client: Optional[AsyncQdrantClient] = None

    async def init(self) -> None:
        """Initialize Qdrant async client."""
        if self._client:
            return
        try:
            self._client = AsyncQdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
            # Quick health check
            await self._client.get_collections()
            logger.info("Connected to Qdrant successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise

    def get_client(self) -> AsyncQdrantClient:
        if not self._client:
            raise RuntimeError("Qdrant client not initialized. Call init() first.")
        return self._client

    async def close(self) -> None:
        # async client has no explicit close, but you can set it to None
        self._client = None
        logger.info("Qdrant client closed.")


# Singleton
qdrant_client = QdrantClient()
