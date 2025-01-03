from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.artist import Artist
from app.schemas.artist import ArtistCreate

# Existing functions
def get_artist(db: Session, artist_id: int):
    return db.query(Artist).filter(Artist.artist_id == artist_id).first()

def create_artist(db: Session, artist: ArtistCreate):
    db_artist = Artist(**artist.dict())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


# 1. SELECT ... WHERE with multiple conditions (e.g., search by country and main_direction)
def get_artists_by_conditions(db: Session, country: str, main_direction: str):
    return db.query(Artist).filter(Artist.country == country, Artist.main_direction == main_direction).all()


# 2. JOIN: Get artists along with their artworks (join Artist and Artwork)
def get_artists_with_artworks(db: Session):
    return db.query(Artist, Artwork).join(Artwork, Artist.artist_id == Artwork.artist_id).all()


# 3. UPDATE with a non-trivial condition (e.g., update country for artists with a specific main direction)
def update_artist_country_by_direction(db: Session, main_direction: str, new_country: str):
    artists_to_update = db.query(Artist).filter(Artist.main_direction == main_direction).all()
    for artist in artists_to_update:
        artist.country = new_country
    db.commit()
    return {"message": f"Updated country for {len(artists_to_update)} artists"}


# 4. GROUP BY: Count artists per country
def group_artists_by_country(db: Session):
    return db.query(Artist.country, func.count(Artist.artist_id).label("count")).group_by(Artist.country).all()


# 5. Sorting: Get sorted artists by a specific field (e.g., sorting by name)
def get_sorted_artists(db: Session, sort_by: str, order: str):
    if order == "asc":
        return db.query(Artist).order_by(getattr(Artist, sort_by).asc()).all()
    elif order == "desc":
        return db.query(Artist).order_by(getattr(Artist, sort_by).desc()).all()
    else:
        return {"message": "Invalid sort order. Use 'asc' or 'desc'."}

