# Eric Liu
# 
# This file contains the logic needed to download and process data, using the functions defined
# in the other files in the data folder

import shutil
import os

from src.functions import make_absolute

from src.data.download_data import download_data
from src.data.process_data import process_data

def run_data(config):
    """
    This file downloads and saves raw and processed data to the folder "data/raw/" and 
    "data/processed/" by default. These save locations can be changed in the config file

    :param:     config      The config file. Default settings can be found in "config/default.json"
    """
    # the folders in which to save data
    data_path = make_absolute(config["data_path"])
    raw_path = data_path + config["raw_folder"]
    adj_close_path = raw_path + config["adj_close_folder"]
    iv_path = raw_path + config["iv_folder"]
    processed_path = data_path + config["processed_folder"]

    # delete then recreate the data folders
    # this is to completly overwrite all data if it exists
    shutil.rmtree(data_path, ignore_errors=True)
    os.mkdir(data_path)
    os.mkdir(raw_path)
    os.mkdir(adj_close_path)
    os.mkdir(iv_path)
    os.mkdir(processed_path)

    # download raw data
    download_data(config)

    # process the data
    process_data(raw_path, processed_path)
