import click
from .cli.project import project

@click.group()
def buildcli():
    """Construction Management CLI System"""
    pass

buildcli.add_command(project)

if __name__ == '__main__':
    buildcli()