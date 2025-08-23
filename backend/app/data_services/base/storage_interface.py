from abc import ABC, abstractmethod

class ImageStorageService(ABC):
    @abstractmethod
    async def upload_image(self, file_bytes: bytes, filename: str) -> str:
        """
        Upload image bytes and return the public URL.
        """
        pass