from datetime import datetime, date
from ..utils.database import get_session
from ..models.project import Project, Phase, Milestone

class ProjectService:
    def create_project(self, name, budget=None, start_date=None, location=None):
        session = get_session()
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
            project = Project(name=name, budget=budget, start_date=start_dt, location=location)
            session.add(project)
            session.commit()
            session.refresh(project)
            return project
        finally:
            session.close()
    
    def list_projects(self, status=None):
        session = get_session()
        try:
            query = session.query(Project)
            if status:
                query = query.filter(Project.status == status)
            return query.all()
        finally:
            session.close()
    
    def get_project(self, project_id):
        session = get_session()
        try:
            return session.query(Project).filter(Project.id == project_id).first()
        finally:
            session.close()
    
    def update_project(self, project_id, **kwargs):
        session = get_session()
        try:
            project = session.query(Project).filter(Project.id == project_id).first()
            if project:
                for key, value in kwargs.items():
                    if hasattr(project, key):
                        setattr(project, key, value)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def add_phase(self, name, project_id, duration=None):
        session = get_session()
        try:
            project = session.query(Project).filter(Project.id == project_id).first()
            if not project:
                return None
            
            phase = Phase(name=name, project_id=project_id, duration=duration)
            session.add(phase)
            session.commit()
            session.refresh(phase)
            return phase
        finally:
            session.close()
    
    def list_phases(self, project_id):
        session = get_session()
        try:
            return session.query(Phase).filter(Phase.project_id == project_id).all()
        finally:
            session.close()
    
    def add_milestone(self, name, project_id, target_date=None):
        session = get_session()
        try:
            project = session.query(Project).filter(Project.id == project_id).first()
            if not project:
                return None
            
            target_dt = datetime.strptime(target_date, "%Y-%m-%d").date() if target_date else None
            milestone = Milestone(name=name, project_id=project_id, target_date=target_dt)
            session.add(milestone)
            session.commit()
            session.refresh(milestone)
            return milestone
        finally:
            session.close()
    
    def list_milestones(self, project_id):
        session = get_session()
        try:
            return session.query(Milestone).filter(Milestone.project_id == project_id).all()
        finally:
            session.close()
    
    def complete_milestone(self, milestone_id):
        session = get_session()
        try:
            milestone = session.query(Milestone).filter(Milestone.id == milestone_id).first()
            if milestone:
                milestone.status = "completed"
                milestone.completion_date = date.today()
                session.commit()
                return milestone
            return None
        finally:
            session.close()