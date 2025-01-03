from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud.artwork import (
    get_artwork,
    create_artwork,
    get_artworks_by_conditions,
    get_artworks_with_artists,
    group_artworks_by_material,
    update_artwork_cost,
    get_sorted_artworks,
)
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

# New endpoints

# 1. SELECT ... WHERE (with multiple conditions)
@router.get("/filter/", response_model=list[Artwork])
async def filter_artworks(
    min_cost: float = Query(..., description="Minimum cost of artwork"),
    max_cost: float = Query(..., description="Maximum cost of artwork"),
    material: str = Query(..., description="Material of the artwork"),
    db: Session = next(get_db())
):
    return get_artworks_by_conditions(db, min_cost, max_cost, material)

# 2. JOIN: Get artworks with their artist information
@router.get("/with-artists/")
async def artworks_with_artists(db: Session = next(get_db())):
    return get_artworks_with_artists(db)

# 3. GROUP BY: Group artworks by material and count
@router.get("/group-by-material/")
async def group_artworks(db: Session = next(get_db())):
    return group_artworks_by_material(db)

# 4. UPDATE with a non-trivial condition
@router.put("/update-cost/")
async def update_cost(
    material: str,
    size: str,
    percentage_increase: float,
    db: Session = next(get_db())
):
    updated_artworks = update_artwork_cost(db, material, size, percentage_increase)
    if not updated_artworks:
        raise HTTPException(status_code=404, detail="No artworks found for the specified criteria")
    return updated_artworks

# 5. Sorting
@router.get("/sorted/")
async def get_sorted(
    sort_by: str = Query("cost", description="Field to sort by (e.g., cost, size, material)"),
    order: str = Query("asc", description="Sort order: 'asc' or 'desc'"),
    db: Session = next(get_db())
):
    return get_sorted_artworks(db, sort_by, order)

