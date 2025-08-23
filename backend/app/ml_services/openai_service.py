from app.ml_services.base import ImageProcessingService, TextEmbeddingService
from app.ml_clients.openai_client import caption_image_base64, get_text_embedding
import base64

class OpenAIImageService(ImageProcessingService):
    def process_found_image(self, image_bytes: bytes):
        image_base64 = base64.b64encode(image_bytes)
        caption = caption_image_base64(image_base64)
        embedding = get_text_embedding(caption)
        return {
            "type": "text",
            "embedding": embedding,
            "metadata": {"caption": caption}
        }

class OpenAITextService(TextEmbeddingService):
    def embed_text(self, text: str):
        return get_text_embedding(text)
