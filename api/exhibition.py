from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.crud.exhibition import (
    get_exhibition,
    create_exhibition,
    get_exhibitions_by_conditions,
    get_exhibitions_with_artworks,
    group_exhibitions_by_type,
    update_exhibition_storage_location,
    get_sorted_exhibitions,
)
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

# 1. SELECT ... WHERE with multiple conditions
@router.get("/filter/", response_model=List[Exhibition])
async def filter_exhibitions(country: str, type_: str, db: Session = next(get_db())):
    return get_exhibitions_by_conditions(db, country=country, type_=type_)

# 2. JOIN: Get exhibitions with artwork details
@router.get("/with-artworks/")
async def list_exhibitions_with_artworks(db: Session = next(get_db())):
    exhibitions = get_exhibitions_with_artworks(db)
    return [{"exhibition": e[0], "artwork": e[1]} for e in exhibitions]

# 3. GROUP BY: Group exhibitions by type
@router.get("/group-by-type/")
async def group_by_type(db: Session = next(get_db())):
    return group_exhibitions_by_type(db)

# 4. UPDATE with a non-trivial condition
@router.put("/update-location/")
async def update_storage_location(country: str, new_location: str, db: Session = next(get_db())):
    updated_exhibitions = update_exhibition_storage_location(db, country=country, new_location=new_location)
    return {"updated_exhibitions": updated_exhibitions}

# 5. Sorting: Get sorted exhibitions
@router.get("/sorted/", response_model=List[Exhibition])
async def sorted_exhibitions(sort_by: str = Query(...), order: str = Query("asc"), db: Session = next(get_db())):
    return get_sorted_exhibitions(db, sort_by=sort_by, order=order)

