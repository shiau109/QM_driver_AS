import xarray as xr

# Assume ds1, ds2, and ds3 are xarray.Dataset objects you have previously created or loaded
ds1 = xr.Dataset()
datasets = [ds1, ds2, ds3]

# Merging the datasets
merged_dataset = xr.merge(datasets)
# Concatenating datasets along a new dimension (e.g., 'time')
concatenated_dataset = xr.concat(datasets, dim='time')
# Now, merged_dataset is a single xarray.Dataset containing all the data from ds1, ds2, and ds3
print(merged_dataset)
