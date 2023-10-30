from sqlalchemy import Column, Integer, String, ForeignKey, Double, Date
from database import Base


class Location(Base):
    __tablename__ = "location"
<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    latitude = Column(Double)
    longitude = Column(Double)
    created_at = Column(Date)
    country_id = Column(Integer, ForeignKey("Country.id"))
=======

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    latitude = Column(Double)
    longitude = Column(Double)
    created_at = Column(DateTime(timezone=True))
    country_id = Column(Integer, ForeignKey("country.id"))

    # Relación con la tabla 'User' si tienes una relación entre 'User' y 'Location'
    creator = relationship("User", back_populates="locations")
>>>>>>> 36050c65bf0dde376e65b48abb4b28fb099d16c2
