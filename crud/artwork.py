from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.artwork import Artwork
from app.models.artist import Artist
from app.schemas.artwork import ArtworkCreate

def get_artwork(db: Session, artwork_id: int):
    return db.query(Artwork).filter(Artwork.artwork_id == artwork_id).first()

def create_artwork(db: Session, artwork: ArtworkCreate):
    db_artwork = Artwork(**artwork.dict())
    db.add(db_artwork)
    db.commit()
    db.refresh(db_artwork)
    return db_artwork

# New functionality

# 1. SELECT ... WHERE (with multiple conditions)
def get_artworks_by_conditions(db: Session, min_cost: float, max_cost: float, material: str):
    return db.query(Artwork).filter(
        Artwork.cost >= min_cost,
        Artwork.cost <= max_cost,
        Artwork.material == material
    ).all()

# 2. JOIN: Get artworks with their artist information
def get_artworks_with_artists(db: Session):
    return db.query(Artwork, Artist).join(Artist, Artwork.artist_id == Artist.artist_id).all()

# 3. GROUP BY: Group artworks by material and count
def group_artworks_by_material(db: Session):
    return db.query(Artwork.material, func.count(Artwork.artwork_id).label("count")).group_by(Artwork.material).all()

# 4. UPDATE with a non-trivial condition: Update artwork cost if it matches a specific material and size
def update_artwork_cost(db: Session, material: str, size: str, percentage_increase: float):
    artworks = db.query(Artwork).filter(
        Artwork.material == material,
        Artwork.size == size
    ).all()
    for artwork in artworks:
        artwork.cost *= (1 + percentage_increase / 100)
    db.commit()
    return artworks

# 5. Sorting: Get artworks sorted by a specified field
def get_sorted_artworks(db: Session, sort_by: str, order: str = "asc"):
    if order == "asc":
        return db.query(Artwork).order_by(getattr(Artwork, sort_by).asc()).all()
    else:
        return db.query(Artwork).order_by(getattr(Artwork, sort_by).desc()).all()

