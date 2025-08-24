# app/infra/database.py
import asyncpg
import logging
from typing import Optional
from app.config.settings import settings

logger = logging.getLogger(__name__)

class Database:
    
    _pool: Optional[asyncpg.Pool] = None
    _active_dsn: Optional[str] = None

    async def init(self) -> None:
        """
        Initializes the database connection pool. It tries a direct connection first,
        then falls back to a pooler URL if available.
        Raises a RuntimeError if all connection attempts fail.
        """
        if self._pool:
            return

        urls_to_try = []
        if not settings.DB_FORCE_POOLER and settings.SUPABASE_DB_DIRECT_URL:
            urls_to_try.append(settings.SUPABASE_DB_DIRECT_URL)
        if settings.SUPABASE_DB_POOLER_URL:
            urls_to_try.append(settings.SUPABASE_DB_POOLER_URL)

        if not urls_to_try:
            raise RuntimeError("No database DSN configured. Set SUPABASE_DB_DIRECT_URL or SUPABASE_DB_POOLER_URL.")

        connection_errors = []
        for dsn in urls_to_try:
            try:
                self._pool = await asyncpg.create_pool(
                    dsn,
                    min_size=1,
                    max_size=settings.DB_POOL_SIZE
                )
                self._active_dsn = dsn
                logger.info(f"Successfully connected to database using: {dsn[:35]}...")
                return
            except Exception as e:
                error_message = f"Failed to connect to database using {dsn[:35]}...: {e}"
                logger.warning(error_message)
                connection_errors.append(error_message)
        
        # If we get here, all URLs failed
        raise RuntimeError(f"Failed to create database pool with any configured URL. Errors: {'; '.join(connection_errors)}")

    async def close(self) -> None:
        """Closes the database connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            self._active_dsn = None
            logger.info("Database connection pool closed.")

    def get_connection(self):
        """
        Acquires a connection from the pool. Use as an async context manager.
        Example: `async with db.get_connection() as conn:`
        """
        if not self._pool:
            raise RuntimeError("Database pool not initialized. Call `await db.init()` first.")
        return self._pool.acquire()

# The singleton instance of the Database class.
# Other parts of the application should import this `db` object.
db = Database()