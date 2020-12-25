# Eric Liu
# 
# This file contains the logic needed to download and process data, using the functions defined
# in the other files in the data folder

import shutil

from src.functions import get_path

from src.data.download_data import download_data
from src.data.process_data import process_data

def run_data(tickers):
    """
    This file downloads and saves raw and processed data to the folder "data/raw/" and 
    "data/processed/" by default. These save locations can be changed in the config file
    """
    # the folders in which to save data
    raw_path = "data/raw/"
    processed_path = "data/processed/"

    # delete then recreate the data folders
    # this is to completly overwrite all data if it exists


    # convert the paths to absoltue paths
    raw_path = get_path(raw_path)
    processed_path = get_path(processed_path)

    # download raw data
    download_data(raw_path, tickers)

    # process the data
    process_data(raw_path, processed_path)
