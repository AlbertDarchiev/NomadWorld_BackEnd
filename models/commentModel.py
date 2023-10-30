from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base

class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location")
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True))