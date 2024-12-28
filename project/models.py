from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Artist(Base):
    tablename = "artist"
    artist_id = Column(Integer, primary_key=True)
    fio = Column(String)
    country = Column(String)
    years_of_life = Column(String)
    main_direction = Column(String)

class Artwork(Base):
    tablename = "artwork"
    artwork_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey("artist.artist_id"))
    name = Column(String)
    type = Column(String)
    cost = Column(Decimal(10, 2))
    size = Column(String)
    material = Column(String)

class Exhibition(Base):
    tablename = "exhibition"
    exhibition_id = Column(Integer, primary_key=True)
    artwork_id = Column(Integer, ForeignKey("artwork.artwork_id"))
    name = Column(String)
    type = Column(String)
    date = Column(Date)
    country = Column(String)
    storage_location = Column(String)
