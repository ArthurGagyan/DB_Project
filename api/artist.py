from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.crud.artist import get_artist, create_artist
from app.schemas.artist import Artist, ArtistCreate
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{artist_id}", response_model=Artist)
async def read_artist(artist_id: int, db: Session = next(get_db())):
    db_artist = get_artist(db, artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist

@router.post("/", response_model=Artist)
async def create_new_artist(artist: ArtistCreate, db: Session = next(get_db())):
    return create_artist(db, artist)
