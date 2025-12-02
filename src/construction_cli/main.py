import click

@click.command()
def buildcli():
    """Construction Management CLI System"""
    click.echo("Welcome to Construction CLI!")

if __name__ == '__main__':
    buildcli()