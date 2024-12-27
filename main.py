from fastapi import FastAPI
from app.routes import items
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)
