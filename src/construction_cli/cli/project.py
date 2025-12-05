import click
from ..utils.database import init_db
from ..services.project_service import ProjectService

@click.group()
def project():
    """Project management commands"""
    pass

@project.command()
def create():
    """Create a new project"""
    init_db()
    
    click.echo("\n=== Create New Project ===")
    name = click.prompt("Project name")
    
    budget_input = click.prompt("Budget (optional, press Enter to skip)", default="", show_default=False)
    budget = None
    if budget_input.strip():
        try:
            budget = float(budget_input)
            if budget < 0:
                click.echo("Budget cannot be negative, project will be created without budget")
                budget = None
        except ValueError:
            click.echo("Invalid budget format, project will be created without budget")
    
    start_date_input = click.prompt("Start date YYYY-MM-DD (optional, press Enter to skip)", default="", show_default=False)
    start_date = None
    if start_date_input.strip():
        try:
            from datetime import datetime
            datetime.strptime(start_date_input, "%Y-%m-%d")
            start_date = start_date_input
        except ValueError:
            click.echo("Invalid date format, project will be created without start date")
    
    location = click.prompt("Project location (optional, press Enter to skip)", default="", show_default=False)
    location = location if location.strip() else None
    
    service = ProjectService()
    project = service.create_project(name, budget, start_date, location)
    
    click.echo("\n✅ Project created successfully!")
    click.echo(f"Name: {name}")
    click.echo(f"ID: {project.id}")
    if budget:
        click.echo(f"Budget: ${budget:,.2f}")
    if location:
        click.echo(f"Location: {location}")
    if start_date:
        click.echo(f"Start Date: {start_date}")

@project.command()
@click.option('--status', help='Filter by status')
def list(status):
    """List all projects"""
    service = ProjectService()
    projects = service.list_projects(status)
    
    if not projects:
        click.echo("No projects found")
        return
    
    click.echo("Project List:")
    for p in projects:
        budget = f"${p.budget:,.0f}" if p.budget else "N/A"
        click.echo(f"{p.id}. {p.name} - {budget} - {p.status}")

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
def add():
    """Add a phase to a project"""
    service = ProjectService()
    
    # Show available projects
    projects = service.list_projects()
    if not projects:
        click.echo("No projects found. Create a project first.")
        return
    
    click.echo("\n=== Add Project Phase ===")
    click.echo("Available projects:")
    for p in projects:
        budget = f"${p.budget:,.0f}" if p.budget else "No budget"
        click.echo(f"  {p.id}. {p.name} - {budget}")
    
    # Select project
    while True:
        try:
            project_id = click.prompt("\nEnter project ID", type=int)
            project = service.get_project(project_id)
            if project:
                break
            else:
                click.echo("Invalid project ID. Please try again.")
        except (ValueError, click.ClickException):
            click.echo("Please enter a valid number")
    
    name = click.prompt("Phase name (e.g., Foundation, Framing, Finishing)")
    
    duration_input = click.prompt("Duration in days (optional, press Enter to skip)", default="", show_default=False)
    duration = None
    if duration_input.strip():
        try:
            duration = int(duration_input)
        except ValueError:
            click.echo("Invalid duration format, phase will be created without duration")
    
    phase = service.add_phase(name, project_id, duration)
    
    click.echo("\n✅ Phase added successfully!")
    click.echo(f"Phase: {name}")
    click.echo(f"ID: {phase.id}")
    click.echo(f"Project: {project.name}")
    if duration:
        click.echo(f"Duration: {duration} days")

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

@click.group()
def milestones():
    """Project milestones management"""
    pass

@milestones.command()
def add():
    """Add a milestone to a project"""
    service = ProjectService()
    
    # Show available projects
    projects = service.list_projects()
    if not projects:
        click.echo("No projects found. Create a project first.")
        return
    
    click.echo("\n=== Add Project Milestone ===")
    click.echo("Available projects:")
    for p in projects:
        budget = f"${p.budget:,.0f}" if p.budget else "No budget"
        click.echo(f"  {p.id}. {p.name} - {budget}")
    
    # Select project
    while True:
        try:
            project_id = click.prompt("\nEnter project ID", type=int)
            project = service.get_project(project_id)
            if project:
                break
            else:
                click.echo("Invalid project ID. Please try again.")
        except (ValueError, click.ClickException):
            click.echo("Please enter a valid number")
    
    name = click.prompt("Milestone name (e.g., Foundation Complete, Grand Opening)")
    
    target_date_input = click.prompt("Target date YYYY-MM-DD (optional, press Enter to skip)", default="", show_default=False)
    target_date = None
    if target_date_input.strip():
        try:
            from datetime import datetime
            datetime.strptime(target_date_input, "%Y-%m-%d")
            target_date = target_date_input
        except ValueError:
            click.echo("Invalid date format, milestone will be created without target date")
    
    milestone = service.add_milestone(name, project_id, target_date)
    
    click.echo("\n✅ Milestone added successfully!")
    click.echo(f"Milestone: {name}")
    click.echo(f"ID: {milestone.id}")
    click.echo(f"Project: {project.name}")
    if target_date:
        click.echo(f"Target date: {target_date}")

@milestones.command()
@click.option('--project-id', required=True, type=int, help='Project ID')
def list(project_id):
    """List milestones for a project"""
    session = get_session()
    try:
        project = session.query(Project).filter(Project.id == project_id).first()
        if not project:
            click.echo("Project not found")
            return
        
        milestones = session.query(Milestone).filter(Milestone.project_id == project_id).all()
        if not milestones:
            click.echo(f"No milestones found for project: {project.name}")
            return
        
        click.echo(f"Milestones for project: {project.name}")
        for m in milestones:
            target = m.target_date.strftime("%Y-%m-%d") if m.target_date else "N/A"
            completion = m.completion_date.strftime("%Y-%m-%d") if m.completion_date else "N/A"
            click.echo(f"{m.id}. {m.name} - Target: {target} - Status: {m.status}")
    finally:
        session.close()

@milestones.command()
@click.option('--milestone-id', required=True, type=int, help='Milestone ID')
def complete(milestone_id):
    """Mark milestone as completed"""
    from datetime import date
    session = get_session()
    try:
        milestone = session.query(Milestone).filter(Milestone.id == milestone_id).first()
        if not milestone:
            click.echo("Milestone not found")
            return
        
        milestone.status = "completed"
        milestone.completion_date = date.today()
        session.commit()
        click.echo(f"Milestone '{milestone.name}' marked as completed")
    finally:
        session.close()

project.add_command(phases)
project.add_command(milestones)