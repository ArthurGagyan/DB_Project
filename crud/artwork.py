from sqlalchemy.orm import Session
from app.models.artwork import Artwork
from app.schemas.artwork import ArtworkCreate

def get_artwork(db: Session, artwork_id: int):
    return db.query(Artwork).filter(Artwork.artwork_id == artwork_id).first()

def create_artwork(db: Session, artwork: ArtworkCreate):
    db_artwork = Artwork(**artwork.dict())
    db.add(db_artwork)
    db.commit()
    db.refresh(db_artwork)
    return db_artwork
