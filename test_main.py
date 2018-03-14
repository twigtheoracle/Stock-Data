from data import Data
from pprint import pprint

d = Data(["AAPL"])
d.retrieve_data(data_provider = "AV")

pprint(d.data)

# test_dict = {"test1": "content1", "test2": "content2", "test3": "content3"}

# keys = test_dict.keys()

# print(type(keys), keys)

# list_keys = list(keys)

# print(type(list_keys), list_keys)