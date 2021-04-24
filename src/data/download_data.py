# Eric Liu
# 
# This file contains the logic needed to download all the raw data for each ticker. This logic is 
# collated in the function download_data

from calendar import monthrange
from tqdm import tqdm

import datetime
import quandl
import os

import numpy as np
import pandas as pd

from src.functions import make_absolute

def download_data(config):
    """
    Download the raw data needed for every ticker

    :param:     config      The config file
    """
    # the folders in which to save data
    data_path = make_absolute(config["data_path"])
    raw_path = data_path + config["raw_folder"]
    adj_close_path = raw_path + config["adj_close_folder"]
    iv_path = raw_path + config["iv_folder"]

    # initialize quandl with the api key
    quandl.ApiConfig.api_key = os.environ["QUANDL_API_KEY"]

    print("Downloading data...")

    # store iv metadata here
    iv_metadata = []

    # iterate over each ticker
    for ticker in tqdm(config["tickers"]):
        # this try except should catch tickers that do not exist in Quandl's EOD database
        try:
            # for each ticker download and save adj_close data
            data = get_ticker_adj_close(ticker)
            data.to_csv(adj_close_path + ticker + ".csv", index=False)

            # for each ticker get iv data/metadata
            # save data and store metadata
            data, metadata = get_ticker_iv(ticker)
            data.to_csv(iv_path + ticker + ".csv", index=False)
            iv_metadata.append(metadata)
        except quandl.errors.quandl_error.NotFoundError as e:
            # print out an error statement
            print()
            print(f"Ticker {ticker} does not exist in Quandl's EOD database. It will be removed " +
                "for the rest of the current run.")

            # remove the ticker from the config file
            config["tickers"].remove(ticker)
    
    # save metadata
    iv_metadata = pd.DataFrame(iv_metadata, columns=["ticker", "next_earnings_day", "trading_days",
        "calendar_days", "crush_rate"])
    iv_metadata.to_csv(iv_path + "metadata.csv", index=False)

    print("Done\n")

def get_ticker_adj_close(ticker):
    """
    Get and return the raw adj_close data for a single ticker

    :param:     ticker      The ticker to get data for

    :return:    pandas.df   The data of the ticker formatted with columns "Date", "Adj_Close"
    """
    # get the current date and historical date as strings
    # TODO: adjust for leap year?
    current_date = datetime.date.today()
    historical_date = datetime.date(year=current_date.year-11, month=current_date.month, 
        day=current_date.day)
    current_date = str(current_date)
    historical_date = str(historical_date)  

    # get the data
    data = quandl.get("EOD/" + ticker, start_date=historical_date, end_date=current_date)

    # reset the index so that the date appears as a column
    data = data.reset_index()

    # select and return only the needed columns
    return data[["Date", "Adj_Close"]]

def get_ticker_iv(ticker):
    """
    Get and return the raw iv data for a single ticker and the metadata

    :param:     ticker      The ticker to get data for

    :return:    pandas.df   The data of the ticker formatted with columns "Date", "Iv30Rank",
                            "Iv30Percentile", and "Iv30Rating"
    :return:    []          A list containing metadata for the stock. In order in the list: next
                            earnings day (date), trading days (int), calendar days (int), earnings
                            crush rate (float)
    """
    # get the day four months ago from today
    current_date = datetime.date.today()
    try:
        historical_date = datetime.date(year=current_date.year, month=current_date.month-4, 
            day=current_date.day)
    except ValueError:
        historical_date = datetime.date(year=current_date.year-1, 
            month=(12 - (4 - current_date.month)), day=current_date.day)
    current_date = str(current_date)
    historical_date = str(historical_date) 

    # get the data
    data = quandl.get("QOR/" + ticker, start_date=historical_date, end_date=current_date) 

    # collect the various metadata
    # sometimes, a ValueError is raised if the next earnings report date is not currenlty known
    try:
        last_row = data.tail(1)
        trading_days = last_row["TradingDaysUntilEarnings"].values[0]
        calendar_days = last_row["CalendarDaysUntilEarnings"].values[0]
        next_earnings_day = datetime.date.today() + datetime.timedelta(days=calendar_days)
        crush_rate = last_row["EarningsCrushRate"].values[0]
        metadata = [ticker, next_earnings_day, trading_days, calendar_days, crush_rate]
    except ValueError:
        metadata = [ticker, "Unknown", "Unknown", "Unknown", "Unknown"]

    # get the most recent 60 data points and the columns we want
    data = data.tail(60)
    data = data[["Iv30Rank","Iv30Percentile", "Iv30Rating"]]

    # return the data and metadata
    return (data, metadata)
