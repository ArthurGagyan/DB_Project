from sqlalchemy import Column, Integer, String
from app.database import Base

class Artist(Base):
    __tablename__ = "artist"

    artist_id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, nullable=False)
    country = Column(String, nullable=True)
    years_of_life = Column(String, nullable=True)
    main_direction = Column(String, nullable=True)
