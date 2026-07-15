import pandas as pd
from frictionless import Package

package = Package('datapackages/siafi/datapackage.json')

package_dimentions = {}
resource_dfs = []

for resource in package.resources:
    # get dimentions on the resource, which are all fields that do not start with 'vlr_'
    dimentions = [field.name for field in resource.schema.fields if not field.name.startswith('vlr_')]
    # get facts on the resource, which are all fields that start with 'vlr_'
    facts = [field.name for field in resource.schema.fields if field.name.startswith('vlr_')]
    # other way to filter is to use a schema custom property like `fact_table: true`
    # we must think a better way to do this

    # apend the dimentions to the package_dimentions dictionary to create the link table later
    package_dimentions[resource.name] = dimentions

    # Instanciate data using pandas
    print(f'Processing {resource.name}')
    df = resource.to_pandas()
    # apend the resource dataframe to the resource_dfs list, dropping the facts and duplicates
    # this will be used to create the link table later
    resource_dfs.append(df.copy().drop(columns=facts).drop_duplicates())

    # create a key column using the dimentions, joining them with a pipe character
    key = df[dimentions].astype('string').fillna('').agg('|'.join, axis=1)
    # drop the dimentions columns from the dataframe and insert the key column at the beginning
    df = df.drop(columns=dimentions)
    df.insert(0, f'key_{resource.name}', key)

    # write the fact table (key + facts) to a csv file
    print(f'Writing {resource.name} to datapackages/siafi/data/fact_{resource.name}.csv.gz')
    df.to_csv(f'datapackages/siafi/data/linktable/fact_{resource.name}.csv.gz', index=False)

# create a combined dataframe with all the dimentions from all the resources, dropping duplicates
# this process will create a link table with all the dimentions from all the resources, which can be used to join the fact tables later
# but it has the potencial to be slow and memory intensive, so we need to think a better way to do this
combined_df = pd.concat(resource_dfs, ignore_index=True)

for resource_name, dimentions in package_dimentions.items():
    print(f'Writing {resource_name} to linktable')
    # create a key column using the dimentions, joining them with a pipe character
    key = combined_df[dimentions].astype('string').fillna('').agg('|'.join, axis=1)
    combined_df.insert(0, f'key_{resource_name}', key)

# write the linktable dataframe to a csv file
combined_df.to_csv('datapackages/siafi/data/linktable/linktable.csv.gz', index=False)
