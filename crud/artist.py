from sqlalchemy.orm import Session
from app.models.artist import Artist
from app.schemas.artist import ArtistCreate

def get_artist(db: Session, artist_id: int):
    return db.query(Artist).filter(Artist.artist_id == artist_id).first()

def create_artist(db: Session, artist: ArtistCreate):
    db_artist = Artist(**artist.dict())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist
