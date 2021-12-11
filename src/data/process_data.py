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

def process_data(config):
    """
    This function contains the logic to change raw data into processed data, as described in the 
    file header

    :param:     config      The config file
    """
    print("Processing Data...")

    # the folders in which to download/save data
    data_path = make_absolute(config["data_path"])
    raw_path = os.path.join(data_path, config["raw_folder"])
    adj_close_path = os.path.join(raw_path, config["adj_close_folder"])
    iv_path = os.path.join(raw_path, config["iv_folder"])
    processed_path = os.path.join(data_path, config["processed_folder"])

    # store short term data statistics here
    short_term_stats = pd.DataFrame(columns=["ticker", "n", "mean", "20 Day STD", "40 Day STD",
        "60 Day STD"])

    # iterate over all the raw data
    for ticker in config["tickers"]:
        # open the adj_close csv file and select the most recent 60 rows
        os.path.join(adj_close_path, ticker + ".csv")
        data = pd.read_csv(os.path.join(adj_close_path, 
            ticker + ".csv"))[:60].reset_index(drop=True)
        
        # compute the various short term data stats
        n = 60 
        mean = data["Adj_Close"].mean()
        std_20 = data["Adj_Close"][-20:].std()
        std_40 = data["Adj_Close"][-40:].std()
        std_60 = data["Adj_Close"].std()

        # add the short term stats to the df
        short_term_stats.loc[len(short_term_stats.index)] = [ticker, n, mean, std_20, std_40, 
            std_60]

        # open the iv csv file and add the columns to data
        iv_data = pd.read_csv(os.path.join(iv_path, ticker + ".csv"))
        data[["IV30 %", "IV30 Rank", "IV30 Rating"]] = iv_data[["Iv30Percentile", "Iv30Rank", 
            "Iv30Rating"]]

        # save the combined columns to a csv file
        data.to_csv(os.path.join(processed_path, ticker + ".csv"), index=False)

    # add short term data statistics to the metadata then save
    metadata = pd.read_csv(os.path.join(iv_path, "metadata.csv"))
    metadata = metadata.merge(short_term_stats, on="ticker", how="inner")
    metadata.to_csv(os.path.join(processed_path, "metadata.csv"), index=False)

    # then compute and save the long term data
    # create the structure to hold the data
    percent_change = []
    std = []
    freq = []

    # get the percent change for each ticker
    for ticker in config["tickers"]:
        data = pd.read_csv(os.path.join(adj_close_path, ticker + ".csv"), parse_dates=["Date"])

        # get the percentage change for every month in the last 10 years for the ticker
        monthly = get_monthly_for_stock(data)

        # add the various values to the proper lists
        percent_change.append([ticker] + monthly[0])
        std.append([ticker] + monthly[1])
        freq.append([ticker] + monthly[2])

    # change the lists of lists to dfs
    columns = ["Ticker", "Jan (1)", "Feb (2)", "Mar (3)", "Apr (4)", "May (5)", "Jun (6)", 
        "Jul (7)", "Aug (8)", "Sep (9)", "Oct (10)", "Nov (11)", "Dec (12)"]
    percent_change = pd.DataFrame(percent_change, columns=columns)
    std = pd.DataFrame(std, columns=columns)
    freq = pd.DataFrame(freq, columns=columns)

    # save the long term data
    percent_change.to_csv(os.path.join(make_absolute(processed_path), "perc.csv"), index=False)
    std.to_csv(os.path.join(make_absolute(processed_path), "std.csv"), index=False)
    freq.to_csv(os.path.join(make_absolute(processed_path), "freq.csv"), index=False)

    print("Done\n")

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
        percent_change_per_year = ((end_price - start_price) / start_price) * 100

        # get the average percent changes
        percent_changes.append(percent_change_per_year.sum() / percent_change_per_year.size)

        # get the standard deviations
        std.append(percent_change_per_year.std())

        # get the frequencies
        positive_change = percent_change_per_year > 0
        freq.append((positive_change.sum() / positive_change.size) * 100)

    # return all values
    return [percent_changes, std, freq]
    