# Eric Liu
# 
# This file contains the logic needed to put processed data into the correct sheets, with the proper
# coloring and formatting

from src.functions import make_absolute

from src.data.download_data import download_data
from src.data.process_data import process_data

def run_sheet(config, wb):
    """
    This file downloads and saves raw and processed data to the folder "data/raw/" and 
    "data/processed/" by default. These save locations can be changed in the config file

    :param:     config      The config file. Default settings can be found in "config/default.json"
    :param:     wb          The empty workbook in which to add
    """
    # the folder where processed data can be found
    processed_path = make_absolute(config["data_path"] + config["processed_folder"])

    # download raw data
    download_data(raw_path, tickers)

    # process the data
    process_data(raw_path, processed_path)
