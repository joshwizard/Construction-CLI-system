import click
from .cli.project import project
from .cli.materials import materials
from .utils.database import init_db

@click.group()
def buildcli():
    """Construction Management CLI System"""
    init_db()

# Add all subcommands for flat help display
from .cli.project import create, list as project_list, status, update, phases, milestones
from .utils.database import get_session
from .models.project import Project, Phase, Milestone
from .cli.materials import add, list as materials_list, inventory, stock, order, orders, suppliers

buildcli.add_command(project)
buildcli.add_command(materials)
buildcli.add_command(create, name='project-create')
buildcli.add_command(project_list, name='project-list')
buildcli.add_command(status, name='project-status')
buildcli.add_command(update, name='project-update')
buildcli.add_command(phases, name='project-phases')
buildcli.add_command(milestones, name='project-milestones')
buildcli.add_command(add, name='materials-add')
buildcli.add_command(materials_list, name='materials-list')
buildcli.add_command(inventory, name='materials-inventory')
buildcli.add_command(stock, name='materials-stock')
buildcli.add_command(order, name='materials-order')
buildcli.add_command(orders, name='materials-orders')
buildcli.add_command(suppliers, name='materials-suppliers')

if __name__ == '__main__':
    buildcli()