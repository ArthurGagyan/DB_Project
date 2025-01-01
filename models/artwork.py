from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Artwork(Base):
    __tablename__ = "artwork"

    artwork_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    size = Column(String, nullable=False)
    material = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey("artist.artist_id"), nullable=False)

    artist = relationship("Artist", back_populates="artworks")
