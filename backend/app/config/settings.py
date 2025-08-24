import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    OPENAI_EMBED_MODEL: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-ada-002")

    # Qdrant
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "items")

    # Supabase
    SUPABASE_PROJECT_URL: str = os.getenv("SUPABASE_PROJECT_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    SUPABASE_BUCKET: str = os.getenv("SUPABASE_BUCKET", "found_item_images")
    SUPABASE_DB_DIRECT_URL: str = os.getenv("SUPABASE_DB_DIRECT_URL", "")
    SUPABASE_DB_POOLER_URL: str = os.getenv("SUPABASE_DB_POOLER_URL", "")

    # Database
    DB_FORCE_POOLER: bool = os.getenv("DB_FORCE_POOLER", "false").lower() in {"1","true","yes"}
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))

# Singleton instance
settings = Settings()