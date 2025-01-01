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
