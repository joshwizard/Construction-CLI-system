import click
from ..utils.database import get_session, init_db
from ..models.material import Material, Supplier, Inventory

@click.group()
def materials():
    """Material management commands"""
    pass

@materials.command()
@click.argument('name')
@click.option('--unit', required=True, help='Unit of measurement')
@click.option('--cost-per-unit', type=float, required=True, help='Cost per unit')
@click.option('--supplier', help='Supplier name')
def add(name, unit, cost_per_unit, supplier):
    """Add a new material"""
    init_db()
    session = get_session()
    try:
        supplier_id = None
        if supplier:
            supplier_obj = session.query(Supplier).filter(Supplier.name == supplier).first()
            if not supplier_obj:
                supplier_obj = Supplier(name=supplier)
                session.add(supplier_obj)
                session.flush()
            supplier_id = supplier_obj.id
        
        new_material = Material(name=name, unit=unit, cost_per_unit=cost_per_unit, supplier_id=supplier_id)
        session.add(new_material)
        session.commit()
        click.echo(f"Added material: {name} (ID: {new_material.id})")
        click.echo(f"Unit: {unit}")
        click.echo(f"Cost per unit: ${cost_per_unit:.2f}")
        if supplier:
            click.echo(f"Supplier: {supplier}")
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
@click.option('--low-stock', is_flag=True, help='Show only low stock items')
@click.option('--threshold', type=float, default=10, help='Low stock threshold')
def inventory(low_stock, threshold):
    """Show inventory status"""
    session = get_session()
    try:
        query = session.query(Material, Inventory).outerjoin(Inventory)
        
        if low_stock:
            query = query.filter(Inventory.quantity <= threshold)
        
        results = query.all()
        if not results:
            click.echo("No inventory items found")
            return
        
        click.echo("Inventory Status:")
        for material, inventory in results:
            qty = inventory.quantity if inventory else 0
            location = inventory.location if inventory else "N/A"
            if not low_stock or (inventory and inventory.quantity <= threshold):
                click.echo(f"{material.name}: {qty} {material.unit} - Location: {location}")
    finally:
        session.close()

@materials.command()
@click.option('--material-id', required=True, type=int, help='Material ID')
@click.option('--quantity', required=True, type=float, help='New quantity')
@click.option('--location', default='warehouse', help='Storage location')
def stock(material_id, quantity, location):
    """Update material stock quantity"""
    session = get_session()
    try:
        material = session.query(Material).filter(Material.id == material_id).first()
        if not material:
            click.echo("Material not found")
            return
        
        inventory = session.query(Inventory).filter(Inventory.material_id == material_id).first()
        if inventory:
            inventory.quantity = quantity
            inventory.location = location
        else:
            inventory = Inventory(material_id=material_id, quantity=quantity, location=location)
            session.add(inventory)
        
        session.commit()
        click.echo(f"Updated stock for {material.name}: {quantity} {material.unit}")
        click.echo(f"Location: {location}")
    finally:
        session.close()

@click.group()
def suppliers():
    """Supplier management"""
    pass

@suppliers.command()
@click.argument('name')
@click.option('--contact', help='Contact information')
def add(name, contact):
    """Add a new supplier"""
    session = get_session()
    try:
        new_supplier = Supplier(name=name, contact=contact)
        session.add(new_supplier)
        session.commit()
        click.echo(f"Added supplier: {name} (ID: {new_supplier.id})")
        if contact:
            click.echo(f"Contact: {contact}")
    finally:
        session.close()

@suppliers.command()
def list():
    """List all suppliers"""
    session = get_session()
    try:
        suppliers = session.query(Supplier).all()
        if not suppliers:
            click.echo("No suppliers found")
            return
        
        click.echo("Suppliers List:")
        for s in suppliers:
            contact = s.contact or "N/A"
            click.echo(f"{s.id}. {s.name} - {contact}")
    finally:
        session.close()

materials.add_command(suppliers)