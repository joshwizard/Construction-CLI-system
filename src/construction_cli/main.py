import click
from .cli.project import project
from .cli.materials import materials
from .utils.database import init_db

@click.group()
def buildcli():
    """Construction Management CLI System"""
    init_db()

buildcli.add_command(project)
buildcli.add_command(materials)

if __name__ == '__main__':
    buildcli()