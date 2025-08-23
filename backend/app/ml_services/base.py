from abc import ABC, abstractmethod
from typing import Dict, List

class ImageProcessingService(ABC):
    @abstractmethod
    def process_found_image(self, image_bytes: bytes) -> Dict:
        """
        Process an image from a found item. Return standardized dict with:
        - type: 'text' or 'image'
        - embedding: List[float]
        - metadata (e.g. caption if relevant)
        """
        pass

class TextEmbeddingService(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass