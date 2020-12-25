# Eric Liu
# 
# This file contains the logic needed to download all the raw data for each ticker. This logic is 
# collated in the function download_data

from calendar import monthrange
from tqdm import tqdm

import datetime
import quandl

import numpy as np
import pandas as pd

from src.api_key import get_API_key as key

def download_data(raw_path, tickers):
    """
    Download the raw data needed for every ticker

    :param:     raw_path        The location at which to save raw data
    :param:     tickers         A list containing every ticker to download data for
    """
    # initialize quandl with the api key
    quandl.ApiConfig.api_key = key()

    print("Downloading data")

    # iterate over each ticker
    for ticker in tqdm(tickers):
        # for each ticker download and save data
        data = get_ticker(ticker)
        data.to_csv(raw_path + ticker + ".csv", index=False)

def get_ticker(ticker):
    """
    Get and return the raw data for a single ticker

    :param:     ticker      The ticker to get data for
    :return:    pandas.df   The data of the ticker formatted with columns "Date", "Adj_Close"
    """
    # get the current date and historical date as strings
    # TODO: adjust for leap year?
    current_date = datetime.date.today()
    historical_date = datetime.date(year=current_date.year-10, month=current_date.month, 
        day=current_date.day)
    current_date = str(current_date)
    historical_date = str(historical_date)  

    # get the data
    data = quandl.get("EOD/" + ticker, start_date = historical_date, end_date=current_date)

    # reset the index so that the date appears as a column
    data = data.reset_index()

    # select and return only the needed columns
    return data[["Date", "Adj_Close"]]
