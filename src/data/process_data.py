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
    percent_change = []
    std = []
    freq = []

    # get the percent change for each ticker
    for ticker_file in os.listdir(make_absolute(raw_path)):
        # get the data
        ticker_path = make_absolute(raw_path + ticker_file)
        data = pd.read_csv(ticker_path, parse_dates=["Date"])

        # get the percentage change for every month in the last 10 years for the ticker
        monthly = get_monthly_for_stock(data)

        # get the actual ticker string
        ticker = [ticker_file.split(".")[0]]

        # add the various values to the proper lists
        percent_change.append(ticker + monthly[0])
        std.append(ticker + monthly[1])
        freq.append(ticker + monthly[2])

    # change the lists of lists to dfs
    columns = ["Ticker", "Jan (1)", "Feb (2)", "Mar (3)", "Apr (4)", "May (5)", "Jun (6)", 
        "Jul (7)", "Aug (8)", "Sep (9)", "Oct (10)", "Nov (11)", "Dec (12)"]
    percent_change = pd.DataFrame(percent_change, columns=columns)
    std = pd.DataFrame(std, columns=columns)
    freq = pd.DataFrame(freq, columns=columns)

    # save the long term data
    percent_change.to_csv(make_absolute(processed_path + "percent_changes.csv"), index=False)
    std.to_csv(make_absolute(processed_path + "standard_deviations.csv"), index=False)
    freq.to_csv(make_absolute(processed_path + "frequencies.csv"), index=False)

def get_monthly_for_stock(data):
    """
    Take the input data and compute the historical average percent change/standard deviation/
    frequency positive for every month. This function ignores the most recent month of data and the 
    oldest month of data, just in case they are not complete. This does not matter since data 
    downloading code should get 11 years of data, so a 10 year average change can be easily 
    computed.

    :param:     data        The input data to process

    :return:    [[float],   A list of three float lists. Each float list should contain 12 elements,
                 [float],   one for each month. The first float list contains average monthly 
                 [float]]   change, the second float list contains standard deviation, and the 
                            third float list contains the frequency positive.
    """
    # store values here
    percent_changes = []
    std = []
    freq = []

    # extract the year and month
    data["Year"] = data["Date"].dt.year
    data["Month"] = data["Date"].dt.month 
    data = data.drop(["Date"], axis=1)

    # ignore the first month of data
    first_row = data.iloc[0]
    data = data[~((data["Year"] == first_row["Year"]) & (data["Month"] == first_row["Month"]))]

    # ignore the last month of data
    last_row = data.iloc[len(data.index) - 1]
    data = data[~((data["Year"] == last_row["Year"]) & (data["Month"] == last_row["Month"]))]

    # find the rows where months change
    # first get the rows where a new month starts
    data["diff_1"] = data["Month"].diff(periods=1)
    starts = data["diff_1"] != 0

    # then get the rows where a month ends
    data["diff_-1"] = data["Month"].diff(periods=-1)
    ends = data["diff_-1"] != 0

    # get the rows where a month begins or ends
    data = data[(starts) | (ends)].drop(["diff_1", "diff_-1"], axis=1)

    # iterate over each month
    for month_index in range(1, 13):
        # get the rows we want
        month_data = data[data["Month"] == month_index]

        # get starting and ending values of "Adj_Close" for the ten most recent years
        start_price = month_data.iloc[0::2][-10:].reset_index(drop=True)["Adj_Close"]
        end_price = month_data.iloc[1::2][-10:].reset_index(drop=True)["Adj_Close"]

        # get the percentage change for the month for every year
        percent_change_per_year = (end_price - start_price) / start_price

        # get the average percent changes
        percent_changes.append(percent_change_per_year.sum() / percent_change_per_year.size)

        # get the standard deviations
        std.append(percent_change_per_year.std())

        # get the frequencies
        positive_change = percent_change_per_year > 0
        freq.append(positive_change.sum() / positive_change.size)

    # return all values
    return [percent_changes, std, freq]