from typing import List, Optional
from app.config.settings import settings
from openai import AsyncOpenAI

class OpenAIClient:
    _client: Optional[AsyncOpenAI] = None
    default_prompt: str = """
    Someone found this item and submitted a photo to a lost-and-found system. Write a clear, specific description of the item to help its owner recognize it. Include what the item is, its color, material, any logos, text, or labels, and any visible signs of wear, damage, or customization. Ignore the background. Keep the description under 500 characters.
    """

    async def init(self) -> None:
        """Initialize AsyncOpenAI client (call once at startup or will be lazy-initialized)."""
        if self._client:
            return
        # creating AsyncOpenAI is synchronous, but keep init async for symmetry with infra clients
        self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    def get_client(self) -> AsyncOpenAI:
        if not self._client:
            raise RuntimeError("OpenAI client not initialized. Call `await openai_client.init()` first.")
        return self._client
    
    async def caption_image_base64(self, image_base64: bytes, prompt: str = default_prompt) -> str:
        """
        Use GPT-4o (or other OpenAI vision model) to caption the image.
        """
        client = self.get_client()
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt.strip()},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64.decode()}"
                            },
                        },
                    ],
                }
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content
        if not isinstance(content, str):
            raise ValueError(f"Unexpected content type: {type(content)} → {content}")
        return content.strip()


    async def get_text_embedding(self,text: str) -> List[float]:
        """
        Get a text embedding from OpenAI using the configured model.
        """
        client = self.get_client()
        response = await client.embeddings.create(
            model=settings.OPENAI_EMBED_MODEL,  # e.g. "text-embedding-3-small"
            input=text,
        )
        return response.data[0].embedding

    async def close(self) -> None:
        # AsyncOpenAI doesn't require explicit close, but null it for cleanup
        self._client = None

# Singleton
openai_client = OpenAIClient()