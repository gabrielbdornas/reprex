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
    key = df[dimentions].astype('string').fillna('').agg('|'.join, axis=1)

    resource_df = df.drop(columns=facts).copy()
    resource_df.insert(0, f'key_{resource.name}', key)
    resource_dfs.append(resource_df)

    fact_df = df.drop(columns=dimentions)
    fact_df.insert(0, f'key_{resource.name}', key)
    print(f'Writing {resource.name} to datapackages/siafi/data/fact_{resource.name}.csv.gz')
    fact_df.to_csv(f'datapackages/siafi/data/linktable/fact_{resource.name}.csv.gz', index=False)

combined_df = pd.concat(resource_dfs, ignore_index=True)
combined_df.to_csv('datapackages/siafi/data/linktable/linktable.csv.gz', index=False)

# Padrão de campos iniciados com "val_" são colunas fato (pensar nesta regra).

# Padrão acima pode coexistir com custom fact_table?

# Em case de mais de um datapackage o repo poderá construir ele antes
# (juntando resources) e depois rodar o script
