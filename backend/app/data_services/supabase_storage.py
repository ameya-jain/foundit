import uuid
import asyncio
from app.config.settings import settings
from app.data_services.base.storage_interface import ImageStorageService
from app.infra.supabase_client import supabase_client

class SupabaseStorageService(ImageStorageService):
    async def upload_image(self, file_bytes: bytes, filename: str) -> str:
        loop = asyncio.get_running_loop()
        client = supabase_client.get_client()
        unique_filename = f"{uuid.uuid4()}_{filename}"
        path = f"{unique_filename}"

        try:
            await loop.run_in_executor(
                None,
                lambda: client.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path, file_bytes, {"content-type": "image/jpeg"}
                ),
            )
        except Exception as e:
            raise Exception(f"Image upload failed: {e}")

        return client.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path)
