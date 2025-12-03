import click
from .cli.project import project
from .cli.materials import materials

@click.group()
def buildcli():
    """Construction Management CLI System"""
    pass

buildcli.add_command(project)
buildcli.add_command(materials)

if __name__ == '__main__':
    buildcli()