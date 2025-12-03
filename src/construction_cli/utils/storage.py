import json
import os

DATA_DIR = "data"
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.json")
MATERIALS_FILE = os.path.join(DATA_DIR, "materials.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_projects():
    ensure_data_dir()
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_projects(projects):
    ensure_data_dir()
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=2)

def load_materials():
    ensure_data_dir()
    if os.path.exists(MATERIALS_FILE):
        with open(MATERIALS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_materials(materials):
    ensure_data_dir()
    with open(MATERIALS_FILE, 'w') as f:
        json.dump(materials, f, indent=2)