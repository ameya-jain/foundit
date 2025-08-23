import uuid
from supabase import create_client, Client
from app.data_services.base.storage_interface import ImageStorageService
from app.config.settings import settings

supabase: Client = create_client(settings.SUPABASE_PROJECT_URL, settings.SUPABASE_KEY)

class SupabaseStorageService(ImageStorageService):
    async def test_connection(self) -> bool:
        """Test if the Supabase connection is working."""
        try:
            # Try to list buckets to test the connection
            response = supabase.storage.list_buckets()
            return True
        except Exception as e:
            print(f"Supabase connection test failed: {e}")
            return False

    async def upload_image(self, file_bytes: bytes, filename: str) -> str:
        unique_filename = f"{uuid.uuid4()}_{filename}"
        path = f"{unique_filename}"

        response = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(path, file_bytes, {"content-type": "image/jpeg"})
        if response.get("error"):
            raise Exception(f"Image upload failed: {response['error']['message']}")

        return supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path)
