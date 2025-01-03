from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.exhibition import Exhibition
from app.models.artwork import Artwork
from app.schemas.exhibition import ExhibitionCreate

def get_exhibition(db: Session, exhibition_id: int):
    return db.query(Exhibition).filter(Exhibition.exhibition_id == exhibition_id).first()

def create_exhibition(db: Session, exhibition: ExhibitionCreate):
    db_exhibition = Exhibition(**exhibition.dict())
    db.add(db_exhibition)
    db.commit()
    db.refresh(db_exhibition)
    return db_exhibition

# 1. SELECT ... WHERE with multiple conditions
def get_exhibitions_by_conditions(db: Session, country: str, type_: str):
    return db.query(Exhibition).filter(
        Exhibition.country == country,
        Exhibition.type == type_
    ).all()

# 2. JOIN: Get exhibitions with artwork details
def get_exhibitions_with_artworks(db: Session):
    return db.query(Exhibition, Artwork).join(Artwork, Exhibition.artwork_id == Artwork.artwork_id).all()

# 3. GROUP BY: Group exhibitions by type and count
def group_exhibitions_by_type(db: Session):
    return db.query(
        Exhibition.type,
        func.count(Exhibition.exhibition_id).label("count")
    ).group_by(Exhibition.type).all()

# 4. UPDATE with a non-trivial condition
def update_exhibition_storage_location(db: Session, country: str, new_location: str):
    exhibitions_to_update = db.query(Exhibition).filter(Exhibition.country == country).all()
    for exhibition in exhibitions_to_update:
        exhibition.storage_location = new_location
    db.commit()
    return exhibitions_to_update

# 5. Sorting: Get exhibitions sorted by a specific field
def get_sorted_exhibitions(db: Session, sort_by: str, order: str):
    if order == "desc":
        return db.query(Exhibition).order_by(desc(getattr(Exhibition, sort_by))).all()
    return db.query(Exhibition).order_by(getattr(Exhibition, sort_by)).all()

