from fastapi import FastAPI
from app.api import artist, artwork, exhibition
from app.database import database, engine
from app.models import Base

Base.metadata.create_all(bind=engine)  # Creates tables during development

app = FastAPI()

app.include_router(artist.router, prefix="/artists", tags=["Artists"])
app.include_router(artwork.router, prefix="/artworks", tags=["Artworks"])
app.include_router(exhibition.router, prefix="/exhibitions", tags=["Exhibitions"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
