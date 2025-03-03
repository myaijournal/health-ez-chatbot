import os

folders = [
    "app",
    "app/models",
    "app/routes",
    "app/utils",
    "config",
    "templates"
]

files = {
    "app/__init__.py": "",
    "app/models/__init__.py": "",
    "app/models/patient.py": "",
    "app/routes/__init__.py": "",
    "app/routes/patient_routes.py": "",
    "app/utils/__init__.py": "",
    "app/utils/db.py": "",
    "config/config.py": "",
    "run.py": "",
    ".gitignore": "",
    "README.md": ""
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file, content in files.items():
    with open(file, "w") as f:
        f.write(content)

print("✅ Flask folder structure created!")
