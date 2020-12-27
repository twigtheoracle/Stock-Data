# Eric Liu
# 
# This file contains the logic needed to process raw data into processed data. This function will
# genereate both short term data and long term data. 
#
# Short term data will consist of one file per ticker, with each file being a csv with the Date
# and Adj_Close columns for the most recent 60 data points. Note: 60 trading days is approximately
# three months
# 
# Long term data will consist of three files total, with each file containing a summary of data
# over the last ten years of historical data. The three sheets are average percent change by month,
# average standard deviation by month, and frequency of positive change by month, all of which
# are over 10 years

import os

import pandas as pd

from src.functions import get_path

def process_data(raw_path, processed_path):
    """
    This function contains the logic to change raw data into processed data, as described in the 
    file header

    :param:     raw_path            The path to load raw data
    :param:     processed_path      The path to save processed data
    """
    # first save all the short term data
    # iterate over all the raw data
    for ticker_file in os.listdir(get_path(raw_path)):
        # open the csv file and select the most recent 60 rows
        ticker_path = get_path(raw_path + ticker_file)
        data = pd.read_csv(ticker_path)[-60:]

        # save the short term data in the proper place
        data.to_csv(get_path(processed_path + ticker_file), index=False)
