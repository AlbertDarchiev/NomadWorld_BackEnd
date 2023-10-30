from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base

class route(Base):
    __tablename__ = "route"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    like = Column(Integer)
    country_id = Column(Integer, ForeignKey("country.id"))

    # Relación con la tabla 'User' si tienes una relación entre 'User' y 'Route'
    creator = relationship("User", back_populates="routes")
    country = relationship("Country", back_populates="routes")
