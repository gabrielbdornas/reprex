import pandas as pd
from frictionless import Package

package = Package('datapackages/siafi/datapackage.json')

package_dimentions = {}
resource_dfs = []

for resource in package.resources:
    dimentions = [field.name for field in resource.schema.fields if not field.custom.get('fact_table', False)]
    facts = [field.name for field in resource.schema.fields if field.custom.get('fact_table', False)]
    package_dimentions[resource.name] = dimentions
    print(f'Processing {resource.name}')
    df = resource.to_pandas()
    resource_dfs.append(df.copy().drop(columns=facts))
    key = df[dimentions].astype('string').fillna('').agg('|'.join, axis=1)
    df = df.drop(columns=dimentions)
    df.insert(0, f'key_{resource.name}', key)
    print(f'Writing {resource.name} to datapackages/siafi/data/fact_{resource.name}.csv.gz')
    df.to_csv(f'datapackages/siafi/data/linktable/fact_{resource.name}.csv.gz', index=False)

combined_df = pd.concat(resource_dfs, ignore_index=True)

for resource_name, dimentions in package_dimentions.items():
    print(f'Writing {resource_name} to linktable')
    key = combined_df[dimentions].astype('string').fillna('').agg('|'.join, axis=1)
    combined_df.insert(0, f'key_{resource_name}', key)

combined_df.to_csv('datapackages/siafi/data/linktable/linktable.csv.gz', index=False)
