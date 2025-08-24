import logging
from typing import Optional
from supabase import create_client, Client
from app.config.settings import settings

logger = logging.getLogger(__name__)


class SupabaseClient:
    _client: Optional[Client] = None

    def init(self) -> None:
        """Initialize the Supabase client."""
        if self._client:
            return

        try:
            self._client = create_client(
                settings.SUPABASE_PROJECT_URL,
                settings.SUPABASE_KEY  # use service role for backend ops
            )
            logger.info("Supabase client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise

    def get_client(self) -> Client:
        if not self._client:
            raise RuntimeError("Supabase client not initialized. Call `supabase_client.init()` first.")
        return self._client

    def close(self) -> None:
        """No-op because supabase-py is HTTP based (no persistent connections)."""
        self._client = None
        logger.info("Supabase client closed.")


# Singleton instance
supabase_client = SupabaseClient()
