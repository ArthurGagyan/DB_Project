from sqlalchemy.orm import Session
from app.models.exhibition import Exhibition
from app.schemas.exhibition import ExhibitionCreate

def get_exhibition(db: Session, exhibition_id: int):
    return db.query(Exhibition).filter(Exhibition.exhibition_id == exhibition_id).first()

def create_exhibition(db: Session, exhibition: ExhibitionCreate):
    db_exhibition = Exhibition(**exhibition.dict())
    db.add(db_exhibition)
    db.commit()
    db.refresh(db_exhibition)
    return db_exhibition
