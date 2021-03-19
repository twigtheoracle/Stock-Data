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

from src.functions import make_absolute

def process_data(raw_path, processed_path):
    """
    This function contains the logic to change raw data into processed data, as described in the 
    file header

    :param:     raw_path            The path to load raw data
    :param:     processed_path      The path to save processed data
    """
    # first save all the short term data
    # iterate over all the raw data
    for ticker_file in os.listdir(make_absolute(raw_path)):
        # open the csv file and select the most recent 60 rows
        ticker_path = make_absolute(raw_path + ticker_file)
        data = pd.read_csv(ticker_path)[-60:]

        # save the short term data in the proper place
        data.to_csv(make_absolute(processed_path + ticker_file), index=False)

    # then compute and save the long term data
    # create the structure to hold the data
    months = ["Jan (1)", "Feb (2)", "Mar (3)", "Apr (4)", "May (5)", "Jun (6)", "Jul (7)", 
        "Aug (8)", "Sep (9)", "Oct (10)", "Nov (11)", "Dec (12)"]
    percent_change = pd.DataFrame(columns=["Ticker"]+months)
    std = pd.DataFrame(columns=["Ticker"]+months)
    freq = pd.DataFrame(columns=["Ticker"]+months)

    # get the percent change for each ticker
    for ticker_file in os.listdir(make_absolute(raw_path)):
        # get the data
        ticker_path = make_absolute(raw_path + ticker_file)
        data = pd.read_csv(ticker_path, parse_dates=["Date"])

        # get the percentage change for every month in the last ~11 years for the ticker
        monthly_changes = get_monthly_percent_change(data)

        # process the monthly percentage change into the various averages/freqs
        raise ValueError

    # save the long term data
    percent_change.to_csv(make_absolute(processed_path + "percent_change.csv"), index=False)
    std.to_csv(make_absolute(processed_path + "std.csv"), index=False)
    freq.to_csv(make_absolute(processed_path + "freq.csv"), index=False)

def get_monthly_percent_change(data):
    """
    Takes the input price data (with dates) and computes the percent change for all available
    months, then returns it as a df. This function will ignore the current month since data is very
    likely not complete. This function will also ignore the first month in the data, since that data
    is also likely not complete. Since 11 months of data are downloaded initially, ignoring those 
    two months does not matter.

    :param:     data        The input data to process

    :return:    pd.df       The data changed to get the percent change for every month
    """
    # extract the year and month
    data["Year"] = data["Date"].dt.year
    data["Month"] = data["Date"].dt.month 
    data = data.drop(["Date"], axis=1)

    # get the year and month of the first row of data


    # get the year and month of the last row of data


    # remove the first and last months of the data

    print(data)