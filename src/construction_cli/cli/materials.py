import click
from ..utils.database import init_db, get_session
from ..services.material_service import MaterialService
from ..models.material import Material, Supplier, Inventory, Order

@click.group()
def materials():
    """Material management commands"""
    pass

@materials.command()
def add():
    """Add a new material"""
    init_db()
    
    click.echo("\n=== Add New Material ===")
    name = click.prompt("Material name")
    unit = click.prompt("Unit of measurement (e.g., cubic-yard, ton, piece)")
    
    while True:
        try:
            cost_per_unit = click.prompt("Cost per unit", type=float)
            break
        except click.BadParameter:
            click.echo("Please enter a valid number")
    
    supplier = click.prompt("Supplier name (optional, press Enter to skip)", default="", show_default=False)
    supplier = supplier if supplier.strip() else None
    
    service = MaterialService()
    material = service.add_material(name, unit, cost_per_unit, supplier)
    
    click.echo("\nMaterial added successfully!")
    click.echo(f"Name: {name}")
    click.echo(f"ID: {material.id}")
    click.echo(f"Unit: {unit}")
    click.echo(f"Cost per unit: ${cost_per_unit:.2f}")
    if supplier:
        click.echo(f"Supplier: {supplier}")

@materials.command()
def list():
    """List all materials"""
    service = MaterialService()
    materials = service.list_materials()
    
    if not materials:
        click.echo("No materials found")
        return
    
    click.echo("Materials List:")
    for m in materials:
        click.echo(f"{m.id}. {m.name} - {m.unit} - ${m.cost_per_unit:.2f}")

@materials.command()
@click.option('--low-stock', is_flag=True, help='Show only low stock items')
@click.option('--threshold', type=float, default=10, help='Low stock threshold')
def inventory(low_stock, threshold):
    """Show inventory status"""
    service = MaterialService()
    results = service.get_inventory(threshold if low_stock else None)
    
    if not results:
        click.echo("No inventory items found")
        return
    
    click.echo("Inventory Status:")
    for material, inventory in results:
        qty = inventory.quantity if inventory else 0
        location = inventory.location if inventory else "N/A"
        click.echo(f"{material.name}: {qty} {material.unit} - Location: {location}")

@materials.command()
def stock():
    """Update material stock quantity"""
    service = MaterialService()
    
    # Show available materials first
    materials = service.list_materials()
    if not materials:
        click.echo("No materials found. Add materials first.")
        return
    
    click.echo("\n=== Update Stock ===")
    click.echo("Available materials:")
    for m in materials:
        click.echo(f"  {m.id}. {m.name} ({m.unit})")
    
    while True:
        try:
            material_id = click.prompt("\nEnter material ID", type=int)
            material = next((m for m in materials if m.id == material_id), None)
            if material:
                break
            else:
                click.echo("Invalid material ID. Please try again.")
        except click.BadParameter:
            click.echo("Please enter a valid number")
    
    while True:
        try:
            quantity = click.prompt(f"Enter quantity ({material.unit})", type=float)
            break
        except click.BadParameter:
            click.echo("Please enter a valid number")
    
    location = click.prompt("Storage location", default="warehouse")
    
    inventory = service.update_stock(material_id, quantity, location)
    
    if inventory:
        click.echo("\nStock updated successfully!")
        click.echo(f"Material: {material.name}")
        click.echo(f"Quantity: {quantity} {material.unit}")
        click.echo(f"Location: {location}")
    else:
        click.echo("\nFailed to update stock")

@click.group()
def suppliers():
    """Supplier management"""
    pass

@suppliers.command()
def add():
    """Add a new supplier"""
    click.echo("\n=== Add New Supplier ===")
    name = click.prompt("Supplier name")
    contact = click.prompt("Contact information (optional, press Enter to skip)", default="", show_default=False)
    contact = contact if contact.strip() else None
    
    service = MaterialService()
    supplier = service.add_supplier(name, contact)
    
    click.echo("\nSupplier added successfully!")
    click.echo(f"Name: {name}")
    click.echo(f"ID: {supplier.id}")
    if contact:
        click.echo(f"Contact: {contact}")

@suppliers.command()
def list():
    """List all suppliers"""
    service = MaterialService()
    suppliers = service.list_suppliers()
    
    if not suppliers:
        click.echo("No suppliers found")
        return
    
    click.echo("Suppliers List:")
    for s in suppliers:
        contact = s.contact or "N/A"
        click.echo(f"{s.id}. {s.name} - {contact}")

@materials.command()
def order():
    """Create a material order"""
    from datetime import datetime
    service = MaterialService()
    
    # Show available materials
    materials = service.list_materials()
    if not materials:
        click.echo("No materials found. Add materials first.")
        return
    
    click.echo("\n=== Create Material Order ===")
    click.echo("Available materials:")
    for m in materials:
        click.echo(f"  {m.id}. {m.name} ({m.unit}) - ${m.cost_per_unit:.2f}")
    
    # Select material
    while True:
        try:
            material_id = click.prompt("\nEnter material ID", type=int)
            material = next((m for m in materials if m.id == material_id), None)
            if material:
                break
            else:
                click.echo("Invalid material ID. Please try again.")
        except click.BadParameter:
            click.echo("Please enter a valid number")
    
    # Enter quantity
    while True:
        try:
            quantity = click.prompt(f"Enter quantity ({material.unit})", type=float)
            break
        except click.BadParameter:
            click.echo("Please enter a valid number")
    
    # Show available suppliers
    suppliers = service.list_suppliers()
    supplier_id = None
    
    if suppliers:
        click.echo("\nAvailable suppliers:")
        for s in suppliers:
            click.echo(f"  {s.id}. {s.name} - {s.contact or 'No contact'}")
        
        if material.supplier_id:
            default_supplier = next((s for s in suppliers if s.id == material.supplier_id), None)
            if default_supplier:
                click.echo(f"\nDefault supplier: {default_supplier.name}")
        
        supplier_choice = click.prompt("Enter supplier ID (or press Enter for material's default)", default="", show_default=False)
        if supplier_choice.strip():
            try:
                supplier_id = int(supplier_choice)
            except ValueError:
                click.echo("Invalid supplier ID, using material's default")
    
    # Delivery date
    delivery_date = click.prompt("Delivery date (YYYY-MM-DD, optional)", default="", show_default=False)
    delivery_dt = None
    if delivery_date.strip():
        try:
            delivery_dt = datetime.fromisoformat(delivery_date).date()
        except ValueError:
            click.echo("Invalid date format, order will be created without delivery date")
            delivery_dt = None
    
    # Create order
    order = service.create_order(material_id, quantity, supplier_id, delivery_dt)
    
    if not order:
        click.echo("\nFailed to create order. Check supplier availability.")
        return
    
    # Show success
    supplier = next((s for s in suppliers if s.id == order.supplier_id), None)
    total_cost = quantity * material.cost_per_unit if material.cost_per_unit else 0
    
    click.echo("\nOrder created successfully!")
    click.echo(f"Order ID: {order.id}")
    click.echo(f"Material: {material.name}")
    click.echo(f"Quantity: {quantity} {material.unit}")
    click.echo(f"Supplier: {supplier.name if supplier else 'Unknown'}")
    click.echo(f"Total Cost: ${total_cost:.2f}")
    if delivery_dt:
        click.echo(f"Expected Delivery: {delivery_dt}")

@materials.command()
def orders():
    """List all material orders"""
    service = MaterialService()
    orders = service.list_orders()
    
    if not orders:
        click.echo("No orders found")
        return
    
    click.echo("Material Orders:")
    for order in orders:
        delivery = order.delivery_date.strftime("%Y-%m-%d") if order.delivery_date else "TBD"
        total = order.quantity * order.material.cost_per_unit if order.material.cost_per_unit else 0
        click.echo(f"{order.id}. {order.material.name} - {order.quantity} {order.material.unit} - {order.supplier.name} - ${total:.2f} - {order.status} - Delivery: {delivery}")

@materials.command()
def delete():
    """Delete a material"""
    service = MaterialService()
    
    # Show available materials
    materials = service.list_materials()
    if not materials:
        click.echo("No materials found.")
        return
    
    click.echo("\n=== Delete Material ===")
    click.echo("Available materials:")
    for m in materials:
        click.echo(f"  {m.id}. {m.name} ({m.unit}) - ${m.cost_per_unit:.2f}")
    
    while True:
        try:
            material_id = click.prompt("\nEnter material ID to delete", type=int)
            material = next((m for m in materials if m.id == material_id), None)
            if material:
                break
            else:
                click.echo("Invalid material ID. Please try again.")
        except (ValueError, click.ClickException):
            click.echo("Please enter a valid number")
    
    # Confirm deletion
    if click.confirm(f"Are you sure you want to delete '{material.name}'?"):
        if service.delete_material(material_id):
            click.echo(f"\nMaterial '{material.name}' deleted successfully!")
        else:
            click.echo(f"\nFailed to delete material '{material.name}'")
    else:
        click.echo("\nDeletion cancelled.")

materials.add_command(suppliers)