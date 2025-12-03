from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
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
    inventory = relationship("Inventory", back_populates="material", uselist=False)

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("materials.id"))
    quantity = Column(Float, default=0)
    location = Column(String(100), default="warehouse")
    
    material = relationship("Material", back_populates="inventory")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("materials.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    quantity = Column(Float, nullable=False)
    order_date = Column(Date)
    delivery_date = Column(Date)
    status = Column(String(20), default="pending")
    
    material = relationship("Material")
    supplier = relationship("Supplier")