import click
from ..utils.database import get_session, init_db
from ..models.material import Material

@click.group()
def materials():
    """Material management commands"""
    pass

@materials.command()
@click.argument('name')
@click.option('--unit', required=True, help='Unit of measurement')
@click.option('--cost-per-unit', type=float, required=True, help='Cost per unit')
def add(name, unit, cost_per_unit):
    """Add a new material"""
    init_db()
    session = get_session()
    try:
        new_material = Material(name=name, unit=unit, cost_per_unit=cost_per_unit)
        session.add(new_material)
        session.commit()
        click.echo(f"Added material: {name} (ID: {new_material.id})")
        click.echo(f"Unit: {unit}")
        click.echo(f"Cost per unit: ${cost_per_unit:.2f}")
    finally:
        session.close()

@materials.command()
def list():
    """List all materials"""
    session = get_session()
    try:
        materials = session.query(Material).all()
        if not materials:
            click.echo("No materials found")
            return
        
        click.echo("Materials List:")
        for m in materials:
            click.echo(f"{m.id}. {m.name} - {m.unit} - ${m.cost_per_unit:.2f}")
    finally:
        session.close()

@materials.command()
def inventory():
    """Show inventory status"""
    session = get_session()
    try:
        materials = session.query(Material).all()
        if not materials:
            click.echo("No materials in inventory")
            return
        
        click.echo("Inventory Status:")
        for m in materials:
            click.echo(f"{m.name}: 0 {m.unit}")
    finally:
        session.close()