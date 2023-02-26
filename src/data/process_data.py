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
        std_20 = data["Adj_Close"][:20].std()
        std_40 = data["Adj_Close"][:40].std()
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
    percent_changes = []
    std_pct = []
    freq_pct_positive = []
    monthly_price_std = []

    # get the percent change for each ticker
    for ticker in config["tickers"]:
        data = pd.read_csv(os.path.join(adj_close_path, ticker + ".csv"), parse_dates=["Date"])

        # get the percentage change for every month in the last 10 years for the ticker
        monthly = get_monthly_for_stock(data)

        # add the various values to the proper lists
        percent_changes.append([ticker] + monthly[0])
        std_pct.append([ticker] + monthly[1])
        freq_pct_positive.append([ticker] + monthly[2])
        monthly_price_std.append([ticker] + monthly[3])

    # change the lists of lists to dfs
    columns = ["Ticker", "Jan (1)", "Feb (2)", "Mar (3)", "Apr (4)", "May (5)", "Jun (6)",
               "Jul (7)", "Aug (8)", "Sep (9)", "Oct (10)", "Nov (11)", "Dec (12)"]
    percent_changes = pd.DataFrame(percent_changes, columns=columns)
    std_pct = pd.DataFrame(std_pct, columns=columns)
    freq_pct_positive = pd.DataFrame(freq_pct_positive, columns=columns)
    monthly_price_std = pd.DataFrame(monthly_price_std, columns=columns)

    # save the long term data
    percent_changes.to_csv(
        os.path.join(make_absolute(processed_path), "percent_changes.csv"), index=False)
    std_pct.to_csv(
        os.path.join(make_absolute(processed_path), "std_pct.csv"), index=False)
    freq_pct_positive.to_csv(
        os.path.join(make_absolute(processed_path), "freq_pct_positive.csv"), index=False)
    monthly_price_std.to_csv(
        os.path.join(make_absolute(processed_path), "monthly_price_std.csv"), index=False)

    print("Done\n")


def get_monthly_for_stock(data):
    """
    Take the input data and compute the historical average percent change/standard deviation/
    frequency positive for every month. This function ignores the most recent month of data and the 
    oldest month of data, just in case they are not complete. This does not matter since data 
    downloading code should get 11 years of data, so a 10 year average change can be easily 
    computed.

    Args:
        data: The input data to process

    Returns:
        list[list[float]]: A list of four float lists. Each float list should contain 12 elements,
            one for each month. The first float list contains average monthly change, the second
            float list contains standard deviation of the average monthly change, the third float
            list contains the frequency of positive average monthly change, and the final float
            list contains the normalized monthly standard deviation of price.
    """
    # store values here
    percent_changes = []
    std_pct = []
    freq_pct_positive = []
    monthly_price_std = []

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

    # Now, compute the normalized price standard deviation for each month
    average_price = \
        data[["Year", "Month", "Adj_Close"]].copy(deep=True).groupby(["Year", "Month"]).mean()
    std_price = \
        data[["Year", "Month", "Adj_Close"]].copy(deep=True).groupby(["Year", "Month"]).std()
    normalized_std_price = (std_price / average_price).reset_index(drop=False)
    normalized_std_price = normalized_std_price.groupby("Month").mean().reset_index(drop=False)

    # Just to make sure, sort by month and take the "Adj_Close" column
    normalized_std_price = normalized_std_price.sort_values(by="Month").reset_index(drop=True)
    monthly_price_std = normalized_std_price["Adj_Close"].to_list()

    # find the rows where months change
    # first get the rows where a new month starts
    data["diff_1"] = data["Month"].diff(periods=1)
    starts = data["diff_1"] != 0

    # then get the rows where a month ends
    data["diff_-1"] = data["Month"].diff(periods=-1)
    ends = data["diff_-1"] != 0

    # get the rows where a month begins or ends
    data = data[starts | ends].drop(["diff_1", "diff_-1"], axis=1)

    # Iterate over each month for the percent change stuff
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
        std_pct.append(percent_change_per_year.std())

        # get the frequencies
        positive_change = percent_change_per_year > 0
        freq_pct_positive.append((positive_change.sum() / positive_change.size) * 100)

    # return all values
    return [percent_changes, std_pct, freq_pct_positive, monthly_price_std]
