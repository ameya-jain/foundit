import uuid
import logging
from typing import List, Dict, Optional

from app.data_services.base.postgres_db_interface import ItemRepository
from app.infra.database import Database

logger = logging.getLogger(__name__)


class PostgresRepository(ItemRepository):
    def __init__(self, db: Database):
        self._db = db

    async def insert_found_item(self, item_data: Dict) -> str:
        item_id = str(uuid.uuid4())
        try:
            async with self._db.get_connection() as conn:
                await conn.execute(
                    """
                    INSERT INTO found_items (
                        id, 
                        finder_user_id, 
                        image_bucket, 
                        image_path,
                        caption_text, 
                        caption_model, 
                        found_at, 
                        location_hint, 
                        status
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    """,
                    item_id,
                    item_data.get("finder_user_id"),
                    item_data["image_bucket"],
                    item_data["image_path"],
                    item_data["caption_text"],
                    item_data.get("caption_model"),
                    item_data.get("found_at"),
                    item_data.get("location_hint"),
                    item_data.get("status", "active"),
                )
            return item_id
        except Exception as e:
            logger.error(f"Failed to insert found item: {e}")
            raise

    async def get_found_item_by_id(self, item_id: str) -> Optional[Dict]:
        try:
            async with self._db.get_connection() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT 
                        id, 
                        finder_user_id, 
                        image_bucket, 
                        image_path,
                        caption_text, 
                        caption_model, 
                        found_at, 
                        location_hint, 
                        status,
                        created_at, 
                        updated_at
                    FROM found_items
                    WHERE id = $1
                    """,
                    item_id,
                )
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get found item {item_id}: {e}")
            raise

    async def insert_lost_report(self, report_data: Dict) -> str:
        report_id = str(uuid.uuid4())
        try:
            async with self._db.get_connection() as conn:
                await conn.execute(
                    """
                    INSERT INTO lost_reports (
                        id, 
                        reporter_user_id, 
                        description_text,
                        lost_at, 
                        location_hint, 
                        status
                    )
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    report_id,
                    report_data.get("reporter_user_id"),
                    report_data["description_text"],
                    report_data.get("lost_at"),
                    report_data.get("location_hint"),
                    report_data.get("status", "open"),
                )
            return report_id
        except Exception as e:
            logger.error(f"Failed to insert lost report: {e}")
            raise

    async def get_lost_report_by_id(self, report_id: str) -> Optional[Dict]:
        try:
            async with self._db.get_connection() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT 
                        id, 
                        reporter_user_id, 
                        description_text,
                        lost_at, 
                        location_hint, 
                        status,
                        created_at, 
                        updated_at
                    FROM lost_reports
                    WHERE id = $1
                    """,
                    report_id,
                )
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get lost report {report_id}: {e}")
            raise

    async def insert_matches(self, matches: List[Dict]) -> None:
        if not matches:
            return
        try:
            async with self._db.get_connection() as conn:
                async with conn.transaction():
                    await conn.executemany(
                        """
                        INSERT INTO matches (
                            id, 
                            found_item_id, 
                            lost_report_id, 
                            score, 
                            method
                        )
                        VALUES ($1, $2, $3, $4, $5)
                        """,
                        [
                            (
                                str(uuid.uuid4()),
                                m["found_item_id"],
                                m["lost_report_id"],
                                m["score"],
                                m.get("method"),
                            )
                            for m in matches
                        ],
                    )
        except Exception as e:
            logger.error(f"Failed to insert matches: {e}")
            raise
