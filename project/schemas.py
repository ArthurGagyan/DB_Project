from pydantic import BaseModel
from typing import Optional

class ArtistBase(BaseModel):
    fio: str
    country: Optional[str] = None
    years_of_life: Optional[str] = None
    main_direction: Optional[str] = None

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    artist_id: int

    class Config:
        orm_mode = True

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
