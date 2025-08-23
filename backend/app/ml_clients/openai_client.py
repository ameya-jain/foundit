import openai
from typing import List
from app.config.settings import settings

openai.api_key = settings.OPENAI_API_KEY

prompt = """
Someone found this item and submitted a photo to a lost-and-found system. Write a clear, specific description of the item to help its owner recognize it. Include what the item is, its color, material, any logos, text, or labels, and any visible signs of wear, damage, or customization. Ignore the background. Keep the description under 500 characters.
"""

def caption_image_base64(image_base64: bytes) -> str:
    """
    Use GPT-4o (or other OpenAI vision model) to caption the image.
    """
    response = openai.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": prompt.strip()},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64.decode()}"}}
                ]
            }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def get_text_embedding(text: str) -> List[float]:
    """
    Get a text embedding from OpenAI using the configured model.
    """
    response = openai.embeddings.create(
        model=settings.OPENAI_EMBED_MODEL,
        input=text
    )
    return response.data[0].embedding
