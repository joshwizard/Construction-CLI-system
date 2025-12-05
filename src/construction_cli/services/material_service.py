from datetime import date
from ..utils.database import get_session
from ..models.material import Material, Supplier, Inventory, Order

class MaterialService:
    def add_material(self, name, unit, cost_per_unit, supplier_name=None):
        session = get_session()
        try:
            supplier_id = None
            if supplier_name:
                supplier = session.query(Supplier).filter(Supplier.name == supplier_name).first()
                if not supplier:
                    supplier = Supplier(name=supplier_name)
                    session.add(supplier)
                    session.flush()
                supplier_id = supplier.id
            
            material = Material(name=name, unit=unit, cost_per_unit=cost_per_unit, supplier_id=supplier_id)
            session.add(material)
            session.commit()
            session.refresh(material)
            return material
        finally:
            session.close()
    
    def list_materials(self):
        session = get_session()
        try:
            return session.query(Material).all()
        finally:
            session.close()
    
    def add_supplier(self, name, contact=None):
        session = get_session()
        try:
            supplier = Supplier(name=name, contact=contact)
            session.add(supplier)
            session.commit()
            session.refresh(supplier)
            return supplier
        finally:
            session.close()
    
    def list_suppliers(self):
        session = get_session()
        try:
            return session.query(Supplier).all()
        finally:
            session.close()
    
    def get_inventory(self, low_stock_threshold=None):
        session = get_session()
        try:
            query = session.query(Material, Inventory).outerjoin(Inventory)
            if low_stock_threshold:
                query = query.filter(Inventory.quantity <= low_stock_threshold)
            return query.all()
        finally:
            session.close()
    
    def update_stock(self, material_id, quantity, location="warehouse"):
        session = get_session()
        try:
            material = session.query(Material).filter(Material.id == material_id).first()
            if not material:
                return None
            
            inventory = session.query(Inventory).filter(Inventory.material_id == material_id).first()
            if inventory:
                inventory.quantity = quantity
                inventory.location = location
            else:
                inventory = Inventory(material_id=material_id, quantity=quantity, location=location)
                session.add(inventory)
            
            session.commit()
            return inventory
        finally:
            session.close()
    
    def create_order(self, material_id, quantity, supplier_id=None, delivery_date=None):
        session = get_session()
        try:
            material = session.query(Material).filter(Material.id == material_id).first()
            if not material:
                return None
            
            if not supplier_id:
                supplier_id = material.supplier_id
            
            if not supplier_id:
                return None
            
            supplier = session.query(Supplier).filter(Supplier.id == supplier_id).first()
            if not supplier:
                return None
            
            order = Order(
                material_id=material_id,
                supplier_id=supplier_id,
                quantity=quantity,
                order_date=date.today(),
                delivery_date=delivery_date
            )
            session.add(order)
            session.commit()
            session.refresh(order)
            return order
        finally:
            session.close()
    
    def list_orders(self):
        session = get_session()
        try:
            return session.query(Order).join(Material).join(Supplier).all()
        finally:
            session.close()