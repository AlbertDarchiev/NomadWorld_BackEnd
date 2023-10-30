from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    latitude = Column(Double)
    longitude = Column(Double)
    created_at = Column(DateTime(timezone=True))
    country_id = Column(Integer, ForeignKey("country.id"))

    # Relación con la tabla 'User' si tienes una relación entre 'User' y 'Location'
    creator = relationship("User", back_populates="locations")
