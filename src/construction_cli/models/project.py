from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
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
    
    phases = relationship("Phase", back_populates="project")
    milestones = relationship("Milestone", back_populates="project")

class Phase(Base):
    __tablename__ = "phases"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(100), nullable=False)
    duration = Column(Integer)
    start_date = Column(Date)
    status = Column(String(20), default="planned")
    
    project = relationship("Project", back_populates="phases")

class Milestone(Base):
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(100), nullable=False)
    target_date = Column(Date)
    completion_date = Column(Date)
    status = Column(String(20), default="pending")
    
    project = relationship("Project", back_populates="milestones")