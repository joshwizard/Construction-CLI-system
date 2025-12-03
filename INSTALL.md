# Construction CLI - Installation Guide

## For End Users (Simple Installation)

### Step 1: Install Python
- Download Python from https://python.org (version 3.8 or higher)
- During installation, check "Add Python to PATH"

### Step 2: Install Construction CLI
Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:
```bash
pip install -e /path/to/Construction
```

### Step 3: Start Using
After installation, you can use `buildcli` from anywhere:
```bash
buildcli --help
```

## Quick Start Examples

### Create Your First Project
```bash
buildcli project create "My House" --budget 250000 --location "123 Main St"
```

### Add Materials
```bash
buildcli materials add "Concrete" --unit cubic-yard --cost-per-unit 120
buildcli materials add "Lumber" --unit board-foot --cost-per-unit 3.50
```

### Add Suppliers
```bash
buildcli materials suppliers add "Home Depot" --contact "555-0123"
```

### View Everything
```bash
buildcli project list
buildcli materials list
buildcli materials inventory
```

## Common Commands

### Project Management
- `buildcli project create "Name" --budget 100000`
- `buildcli project list`
- `buildcli project status --project-id 1`

### Materials & Inventory
- `buildcli materials add "Material" --unit unit --cost-per-unit 50`
- `buildcli materials inventory`
- `buildcli materials stock --material-id 1 --quantity 100`

### Orders
- `buildcli materials order --material-id 1 --quantity 50`
- `buildcli materials orders`

## Getting Help
- `buildcli --help` - Main help
- `buildcli project --help` - Project commands
- `buildcli materials --help` - Material commands