from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..utils.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact = Column(String(100))
    
    materials = relationship("Material", back_populates="supplier")

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(20))
    cost_per_unit = Column(Float)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    
    supplier = relationship("Supplier", back_populates="materials")