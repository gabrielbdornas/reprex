import tomllib
from frictionless import Package

with open('data.toml', "rb") as f:
    descriptors = tomllib.load(f)

for descriptor in descriptors['datapackages'].values():
    package = Package(descriptor['path'])
    print(f"Package '{package.name}' loaded successfully with {len(package.resources)} resource(s).")
