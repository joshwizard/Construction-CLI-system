# Construction CLI - Project Management Tool

A simple command-line tool for managing construction projects, materials, and suppliers.

## 🚀 Quick Install

### Windows Users
1. Double-click `install.bat`
2. Use `buildcli --help` to get started

### Mac/Linux Users  
1. Run `./install.sh`
2. Use `buildcli --help` to get started

## 📋 What You Can Do

### Manage Projects
- Create and track construction projects
- Set budgets and locations
- Add project phases (Foundation, Framing, etc.)
- Set milestones with target dates

### Manage Materials
- Add materials with costs and suppliers
- Track inventory levels
- Get low-stock alerts
- Create purchase orders

### Manage Suppliers
- Add supplier contact information
- Track which materials come from which suppliers

## 🎯 Example Workflow

```bash
# Create a new project
buildcli project create "Kitchen Renovation" --budget 15000 --location "Home"

# Add some materials
buildcli materials add "Tiles" --unit square-foot --cost-per-unit 4.50
buildcli materials add "Cabinets" --unit piece --cost-per-unit 250

# Add suppliers
buildcli materials suppliers add "Tile World" --contact "555-TILE"

# Check your project
buildcli project list
buildcli materials inventory
```

## 📖 Full Documentation
See `INSTALL.md` for detailed installation and usage instructions.

## 🏗️ Features
- ✅ Project management with budgets
- ✅ Material and supplier tracking  
- ✅ Inventory management
- ✅ Purchase order system
- ✅ Project phases and milestones
- ✅ Cost calculations
- ✅ Low stock alerts