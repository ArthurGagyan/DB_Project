from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.crud.artist import get_artist, create_artist, get_artists_by_conditions, get_artists_with_artworks, update_artist_country_by_direction, group_artists_by_country, get_sorted_artists
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


# 1. SELECT ... WHERE (with multiple conditions)
@router.get("/search/")
async def search_artists(country: str, main_direction: str, db: Session = next(get_db())):
    db_artists = get_artists_by_conditions(db, country, main_direction)
    if not db_artists:
        raise HTTPException(status_code=404, detail="No artists found with the given conditions")
    return db_artists


# 2. JOIN: Get artists along with their artworks
@router.get("/with_artworks/")
async def get_artists_and_artworks(db: Session = next(get_db())):
    db_artists_with_artworks = get_artists_with_artworks(db)
    if not db_artists_with_artworks:
        raise HTTPException(status_code=404, detail="No artists with artworks found")
    return db_artists_with_artworks


# 3. UPDATE: Update artist country based on main direction
@router.put("/update_country/{main_direction}")
async def update_country(main_direction: str, new_country: str, db: Session = next(get_db())):
    result = update_artist_country_by_direction(db, main_direction, new_country)
    return result


# 4. GROUP BY: Group artists by country
@router.get("/group_by_country/")
async def group_artists(db: Session = next(get_db())):
    grouped_artists = group_artists_by_country(db)
    return grouped_artists


# 5. Sorting: Get sorted artists by a specific field
@router.get("/sorted/")
async def sorted_artists(sort_by: str, order: str, db: Session = next(get_db())):
    db_artists = get_sorted_artists(db, sort_by, order)
    if "Invalid sort order" in db_artists:
        raise HTTPException(status_code=400, detail=db_artists["message"])
    return db_artists

