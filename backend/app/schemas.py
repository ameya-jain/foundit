from pydantic import BaseModel

class LostItemInput(BaseModel):
    description: str
    location_hint: str = "unknown"
