from xarray import Dataset, DataArray

def QMM_dataset(dataset:Dataset)->list[DataArray]:
    seperated_dataset = []
    for ro_name, data in dataset.data_vars.items():
        data.attrs = dataset.attrs
        data.name = ro_name
        seperated_dataset.append(data)
    return seperated_dataset