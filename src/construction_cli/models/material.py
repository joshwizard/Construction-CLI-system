from sqlalchemy import Column, Integer, String, Float
from ..utils.database import Base

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(20))
    cost_per_unit = Column(Float)