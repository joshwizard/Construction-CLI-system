import click
from ..utils.database import get_session, init_db
from ..models.project import Project

@click.group()
def project():
    """Project management commands"""
    pass

@project.command()
@click.argument('name')
@click.option('--budget', type=float, help='Project budget')
def create(name, budget):
    """Create a new project"""
    init_db()
    session = get_session()
    try:
        new_project = Project(name=name, budget=budget)
        session.add(new_project)
        session.commit()
        click.echo(f"Created project: {name} (ID: {new_project.id})")
        if budget:
            click.echo(f"Budget: ${budget:,.2f}")
    finally:
        session.close()

@project.command()
def list():
    """List all projects"""
    session = get_session()
    try:
        projects = session.query(Project).all()
        if not projects:
            click.echo("No projects found")
            return
        
        click.echo("Project List:")
        for p in projects:
            budget = f"${p.budget:,.0f}" if p.budget else "N/A"
            click.echo(f"{p.id}. {p.name} - {budget}")
    finally:
        session.close()