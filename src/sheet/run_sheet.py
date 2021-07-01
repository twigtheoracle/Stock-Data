# Eric Liu
# 
# This file contains the logic needed to put processed data into the correct sheets, with the proper
# coloring and formatting

import pandas as pd
from tqdm import tqdm

from src.functions import make_absolute, get_workbook, save

from src.sheet.short_term_sheet import add_short_term_sheet
from src.sheet.long_term_sheet import add_long_term_sheets

def run_sheet(config):
    """
    This file collates the logic needed to put processed data into the sheet

    :param:     config      The config file

    :return:    str         The name of the wb saved
    """
    # the folders in which to get data
    data_path = make_absolute(config["data_path"])
    processed_path = data_path + config["processed_folder"]
    xl_path = make_absolute(config["save_location"])

    # create the wb with the proper pages for each sheet
    wb = get_workbook(config["tickers"])

    # add short term data to the wb

    # get the short term metadata
    metadata = pd.read_csv(processed_path + "metadata.csv")

    # iterate over every ticker with short term data
    print("Adding short term data...")
    for ticker in tqdm(config["tickers"]):
        # get the short term data for this ticker
        data = pd.read_csv(processed_path + ticker + ".csv")

        # add the short term data and metadata to the wb
        add_short_term_sheet(ticker, wb[ticker], data, metadata[metadata["ticker"] == ticker], 
            config)
    print("Done\n")

    print("Adding long term data...")
    # add all long term sheets
    add_long_term_sheets(wb, config)
    print("Done\n")

    # at the end save the sheet
    return save(wb, xl_path)
    