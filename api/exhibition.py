from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.crud.exhibition import get_exhibition, create_exhibition
from app.schemas.exhibition import Exhibition, ExhibitionCreate
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{exhibition_id}", response_model=Exhibition)
async def read_exhibition(exhibition_id: int, db: Session = next(get_db())):
    db_exhibition = get_exhibition(db, exhibition_id=exhibition_id)
    if db_exhibition is None:
        raise HTTPException(status_code=404, detail="Exhibition not found")
    return db_exhibition

@router.post("/", response_model=Exhibition)
async def create_new_exhibition(exhibition: ExhibitionCreate, db: Session = next(get_db())):
    return create_exhibition(db, exhibition)
