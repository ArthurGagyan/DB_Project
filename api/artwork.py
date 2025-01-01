from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.crud.artwork import get_artwork, create_artwork
from app.schemas.artwork import Artwork, ArtworkCreate
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{artwork_id}", response_model=Artwork)
async def read_artwork(artwork_id: int, db: Session = next(get_db())):
    db_artwork = get_artwork(db, artwork_id=artwork_id)
    if db_artwork is None:
        raise HTTPException(status_code=404, detail="Artwork not found")
    return db_artwork

@router.post("/", response_model=Artwork)
async def create_new_artwork(artwork: ArtworkCreate, db: Session = next(get_db())):
    return create_artwork(db, artwork)
