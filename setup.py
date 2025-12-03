from setuptools import setup, find_packages

setup(
    name="construction-cli",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "sqlalchemy>=1.4.0",
    ],
    entry_points={
        "console_scripts": [
            "buildcli=construction_cli.main:buildcli",
        ],
    },
    author="Construction Manager",
    description="A CLI tool for construction project management",
)