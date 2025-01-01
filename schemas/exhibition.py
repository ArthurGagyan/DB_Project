from pydantic import BaseModel
from typing import Optional
from app.schemas.artwork import Artwork

class ExhibitionBase(BaseModel):
    name: str
    type: str
    date: str
    country: str
    storage_location: str

class ExhibitionCreate(ExhibitionBase):
    artwork_id: int

class Exhibition(ExhibitionBase):
    exhibition_id: int
    artwork: Artwork

    class Config:
        orm_mode = True
