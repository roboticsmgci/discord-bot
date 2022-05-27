from json import dump
from json import load


# Read from data file
def read(file, key=None):
    with open(f"data/{file}.json", "r") as json_file:
        if key:
            return load(json_file)[key]
        else:
            return load(json_file)


# Write to data file
def write(file, item):
    with open(f"data/{file}.json", "w") as json_file:
        dump(item, json_file, indent=2)


# Write key-value pairs to data file
def write_value(file, **kwargs):
    data = read(file)
    for kwarg in kwargs:
        data[kwarg] = kwargs[kwarg]
    write(file, data)
