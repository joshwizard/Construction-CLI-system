import click

@click.group()
def project():
    """Project management commands"""
    pass

@project.command()
@click.argument('name')
@click.option('--budget', type=float, help='Project budget')
def create(name, budget):
    """Create a new project"""
    click.echo(f"Created project: {name}")
    if budget:
        click.echo(f"Budget: ${budget:,.2f}")

@project.command()
def list():
    """List all projects"""
    click.echo("Project List:")
    click.echo("1. Sample Project - $100,000")
    click.echo("2. Demo Project - $50,000")