from sqlalchemy import Column, Integer, String, Float, Date
from ..utils.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    budget = Column(Float)
    status = Column(String(20), default="active")