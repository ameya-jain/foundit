from app.ml_services.base import ImageProcessingService, TextEmbeddingService
from app.infra.openai_client import openai_client
import base64

class OpenAIImageService(ImageProcessingService):
    async def process_found_image(self, image_bytes: bytes):
        image_base64 = base64.b64encode(image_bytes)
        caption = await openai_client.caption_image_base64(image_base64)
        embedding = await openai_client.get_text_embedding(caption)
        return {
            "type": "text",
            "embedding": embedding,
            "metadata": {"caption": caption}
        }

class OpenAITextService(TextEmbeddingService):
    async def embed_text(self, text: str):
        return await openai_client.get_text_embedding(text)
