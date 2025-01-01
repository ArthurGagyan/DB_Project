from pydantic import BaseModel
from typing import Optional
from app.schemas.artist import Artist

class ArtworkBase(BaseModel):
    name: str
    type: str
    cost: float
    size: str
    material: str

class ArtworkCreate(ArtworkBase):
    artist_id: int

class Artwork(ArtworkBase):
    artwork_id: int
    artist: Artist

    class Config:
        orm_mode = True
