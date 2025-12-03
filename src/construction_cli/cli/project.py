import click
from ..utils.database import get_session, init_db
from ..models.project import Project, Phase

@click.group()
def project():
    """Project management commands"""
    pass

@project.command()
@click.argument('name')
@click.option('--budget', type=float, help='Project budget')
@click.option('--start-date', help='Start date (YYYY-MM-DD)')
@click.option('--location', help='Project location')
def create(name, budget, start_date, location):
    """Create a new project"""
    from datetime import datetime
    init_db()
    session = get_session()
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
        new_project = Project(name=name, budget=budget, start_date=start_dt, location=location)
        session.add(new_project)
        session.commit()
        click.echo(f"Created project: {name} (ID: {new_project.id})")
        if budget:
            click.echo(f"Budget: ${budget:,.2f}")
        if location:
            click.echo(f"Location: {location}")
    finally:
        session.close()

@project.command()
@click.option('--status', help='Filter by status')
def list(status):
    """List all projects"""
    session = get_session()
    try:
        query = session.query(Project)
        if status:
            query = query.filter(Project.status == status)
        projects = query.all()
        
        if not projects:
            click.echo("No projects found")
            return
        
        click.echo("Project List:")
        for p in projects:
            budget = f"${p.budget:,.0f}" if p.budget else "N/A"
            click.echo(f"{p.id}. {p.name} - {budget} - {p.status}")
    finally:
        session.close()

@project.command()
@click.option('--project-id', required=True, type=int, help='Project ID')
def status(project_id):
    """Show project status"""
    session = get_session()
    try:
        project = session.query(Project).filter(Project.id == project_id).first()
        if not project:
            click.echo("Project not found")
            return
        
        click.echo(f"Project: {project.name}")
        click.echo(f"Status: {project.status}")
        click.echo(f"Budget: ${project.budget:,.0f}" if project.budget else "Budget: N/A")
        click.echo(f"Location: {project.location or 'N/A'}")
        click.echo(f"Start Date: {project.start_date or 'N/A'}")
    finally:
        session.close()

@project.command()
@click.option('--project-id', required=True, type=int, help='Project ID')
@click.option('--budget', type=float, help='New budget')
@click.option('--status', help='New status')
@click.option('--location', help='New location')
def update(project_id, budget, status, location):
    """Update project details"""
    session = get_session()
    try:
        project = session.query(Project).filter(Project.id == project_id).first()
        if not project:
            click.echo("Project not found")
            return
        
        if budget:
            project.budget = budget
        if status:
            project.status = status
        if location:
            project.location = location
        
        session.commit()
        click.echo("Project updated successfully")
    finally:
        session.close()

@click.group()
def phases():
    """Project phases management"""
    pass

@phases.command()
@click.argument('name')
@click.option('--project-id', required=True, type=int, help='Project ID')
@click.option('--duration', type=int, help='Duration in days')
def add(name, project_id, duration):
    """Add a phase to a project"""
    session = get_session()
    try:
        project = session.query(Project).filter(Project.id == project_id).first()
        if not project:
            click.echo("Project not found")
            return
        
        new_phase = Phase(name=name, project_id=project_id, duration=duration)
        session.add(new_phase)
        session.commit()
        click.echo(f"Added phase: {name} (ID: {new_phase.id}) to project {project.name}")
        if duration:
            click.echo(f"Duration: {duration} days")
    finally:
        session.close()

@phases.command()
@click.option('--project-id', required=True, type=int, help='Project ID')
def list(project_id):
    """List phases for a project"""
    session = get_session()
    try:
        project = session.query(Project).filter(Project.id == project_id).first()
        if not project:
            click.echo("Project not found")
            return
        
        phases = session.query(Phase).filter(Phase.project_id == project_id).all()
        if not phases:
            click.echo(f"No phases found for project: {project.name}")
            return
        
        click.echo(f"Phases for project: {project.name}")
        for p in phases:
            duration = f"{p.duration} days" if p.duration else "N/A"
            click.echo(f"{p.id}. {p.name} - {duration} - {p.status}")
    finally:
        session.close()

project.add_command(phases)