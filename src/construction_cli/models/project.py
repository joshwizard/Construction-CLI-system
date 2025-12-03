from sqlalchemy import Column, Integer, String, Float, Date
from ..utils.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200))
    budget = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20), default="active")