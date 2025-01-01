from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Exhibition(Base):
    __tablename__ = "exhibition"

    exhibition_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    country = Column(String, nullable=False)
    storage_location = Column(String, nullable=False)
    artwork_id = Column(Integer, ForeignKey("artwork.artwork_id"), nullable=False)

    artwork = relationship("Artwork", back_populates="exhibitions")
