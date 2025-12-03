import click

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
    click.echo(f"Added material: {name}")
    click.echo(f"Unit: {unit}")
    click.echo(f"Cost per unit: ${cost_per_unit:.2f}")

@materials.command()
def list():
    """List all materials"""
    click.echo("Materials List:")
    click.echo("1. Concrete - cubic-yard - $120.00")
    click.echo("2. Steel Rebar - ton - $800.00")

@materials.command()
def inventory():
    """Show inventory status"""
    click.echo("Inventory Status:")
    click.echo("Concrete: 50 cubic-yards")
    click.echo("Steel Rebar: 10 tons")