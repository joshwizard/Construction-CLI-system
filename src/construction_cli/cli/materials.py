import click
from ..utils.database import get_session, init_db
from ..models.material import Material, Supplier, Inventory, Order

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

@materials.command()
@click.option('--material-id', required=True, type=int, help='Material ID')
@click.option('--quantity', required=True, type=float, help='Quantity to order')
@click.option('--supplier-id', type=int, help='Supplier ID')
@click.option('--delivery-date', help='Expected delivery date (YYYY-MM-DD)')
def order(material_id, quantity, supplier_id, delivery_date):
    """Create a material order"""
    from datetime import datetime, date
    session = get_session()
    try:
        material = session.query(Material).filter(Material.id == material_id).first()
        if not material:
            click.echo("Material not found")
            return
        
        # Use material's supplier if no supplier specified
        if not supplier_id:
            supplier_id = material.supplier_id
        
        if not supplier_id:
            click.echo("No supplier specified and material has no default supplier")
            return
        
        supplier = session.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            click.echo("Supplier not found")
            return
        
        delivery_dt = datetime.strptime(delivery_date, "%Y-%m-%d").date() if delivery_date else None
        
        new_order = Order(
            material_id=material_id,
            supplier_id=supplier_id,
            quantity=quantity,
            order_date=date.today(),
            delivery_date=delivery_dt
        )
        session.add(new_order)
        session.commit()
        
        total_cost = quantity * material.cost_per_unit if material.cost_per_unit else 0
        click.echo(f"Created order (ID: {new_order.id})")
        click.echo(f"Material: {material.name}")
        click.echo(f"Quantity: {quantity} {material.unit}")
        click.echo(f"Supplier: {supplier.name}")
        click.echo(f"Total Cost: ${total_cost:.2f}")
        if delivery_date:
            click.echo(f"Expected Delivery: {delivery_date}")
    finally:
        session.close()

@materials.command()
def orders():
    """List all material orders"""
    session = get_session()
    try:
        orders = session.query(Order).join(Material).join(Supplier).all()
        if not orders:
            click.echo("No orders found")
            return
        
        click.echo("Material Orders:")
        for order in orders:
            delivery = order.delivery_date.strftime("%Y-%m-%d") if order.delivery_date else "TBD"
            total = order.quantity * order.material.cost_per_unit if order.material.cost_per_unit else 0
            click.echo(f"{order.id}. {order.material.name} - {order.quantity} {order.material.unit} - {order.supplier.name} - ${total:.2f} - {order.status} - Delivery: {delivery}")
    finally:
        session.close()

materials.add_command(suppliers)