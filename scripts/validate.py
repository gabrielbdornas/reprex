from frictionless import Resource

# 1º cenario - Create resource with datapackage.json file
dp_resource = Resource('datapackage.json')
datapakcage_validation = dp_resource.validate()

if datapakcage_validation.valid:
    print("The resource is valid using datapackage.json as descriptor")
else:
    print("The resource is invalid using datapackage.json as descriptor")

# 2º cenario - Create resource with multiple data files and extrapaths parameter
path_resource = Resource('data/example1.csv', extrapaths=['data/example2.csv'])
path_validation = path_resource.validate()

if path_validation.valid:
    print("The resource is valid using multiple data files with extrapaths parameter")
else:
    print("The resource is invalid using multiple data files with extrapaths parameter")

# 3º cenario - Create resource with multiple data files and a datapackage.json file
resource = Resource(name="example", extrapaths=["data/example1.csv", "data/example2.csv"])
resource_validate = resource.validate()

if resource_validate.valid:
    print("The resource is valid using the extrapaths and name parameters")
else:
    print("The resource is invalid using the extrapaths and name parameters.",
          f"The error message is: {resource.validate().tasks[0].errors[0].message}"
    )

