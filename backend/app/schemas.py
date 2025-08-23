from pydantic import BaseModel

class LostItemInput(BaseModel):
    description: str
