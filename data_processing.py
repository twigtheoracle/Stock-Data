import quandl
import numpy as np
import pandas as pd

# used to shift ndarrays forward/backward by index
from scipy.ndimage.interpolation import shift

import datetime

import api_key as key

################################################################################

class Data():

    def __init__(self, sl):
        """
        Initializes the data object with the Quandl API key
        Initializes the data object with a dataframe to store the adjusted 
        closing price of all the stocks
        :param:     sl          a list of the stock tickers to get data from
        """
        # initialize the Quandl key
        quandl.ApiConfig.api_key = key.get_Quandl_API_key()

        # create the dataframe to hold all the data
        self.stocks_long_term_data = pd.DataFrame()

        # create the dataframe to hold the recent data
        self.stocks_short_term_data = pd.DataFrame()

        # store the stock list
        self.stock_list = sl

        # get the relevant dates for today
        self.dates = self.get_dates()

    def get_dates(self):
        """
        Gets the current date and the date 10 years ago
        :param:     None
        :return:    list        [today's date, short term data start, long term 
                                data end, long term data start] as datetime 
                                objects. 
                                note, the exact date varies a bit, look at the 
                                inline comments for more details
        """
        # get the date today and 63 days ago
        # note, 63 trading days is ~ 3 months
        today = datetime.date.today()
        short_term_data_start = today - datetime.timedelta(days=63)

        # get the long term data end
        # this is the last trading day of the previous month
        long_term_data_end = datetime.date(today.year, today.month, 1)
        long_term_data_end -= datetime.timedelta(days=1)     

        # get the long term data start
        # this is the first trading day of the current month ten years ago
        long_term_data_start = datetime.date(today.year - 10, 
            today.month, 1)

        # WARNING: be cautious about leap years and how adding/subtracting days
        # affects the date

        return ([today, short_term_data_start, long_term_data_end, 
            long_term_data_start])

    def get_ticker_data(self, ticker):
        """
        Retrieves all data between today and 10 years ago
        :param:     ticker      the stock to retrieve the data of
        :return:    list        a list containing two dataframes. the first has
                                the short term data (63 days) and the second
                                has the long term data (10 years)
        """
        # get the short term data for the input ticker
        # quandl.get() returns a df
        short_term_data = quandl.get("EOD/" + ticker + ".11", 
            start_date=str(self.dates[1]), 
            end_date=str(self.dates[0]))

        # get the long term data for the input ticker
        # quandl.get() returns a df
        long_term_data = quandl.get("EOD/" + ticker + ".11", 
            start_date=str(self.dates[3]), 
            end_date=str(self.dates[2]))

        # set the name of the only column of both data sets to be the name
        # of the ticker
        short_term_data.columns = [ticker]
        long_term_data.columns = [ticker]

        # TODO: check for missing data and impute as necessary
        # may not be necessary?

        return [short_term_data, long_term_data]

    def get_data(self):
        """
        Gets the data for all the input stocks and aligns them correctly by date
        :param:     None
        :return:    None
        """
        # iterate over the stock list
        for stock in self.stock_list:
            # get the data for this stock
            stock_data = self.get_ticker_data(stock)

            # combine the short term data of this stock with the master df of 
            # all short term data
            # uses concat row-wise (axis=1), joining all data, without sorting
            self.stocks_short_term_data = pd.concat(
                [self.stocks_short_term_data, stock_data[0]], 
                axis=1, join="outer", sort=False)

            # combine the long term data of this stock with the master df of 
            # all long term data
            # uses concat row-wise (axis=1), joining all data, without sorting
            self.stocks_long_term_data = pd.concat(
                [self.stocks_long_term_data, stock_data[1]], 
                axis=1, join="outer", sort=False)

        # remove rows from all data such that the last row is the last trading
        # day of the previous month

        print("Long Term Data")
        print(self.stocks_long_term_data)
        print()
        print("Short Term Data")
        print(self.stocks_short_term_data)

    def cut_long_term_data(self):
        """
        Cuts out rows of the long term data such that for any given month, the
        only remaining rows are the first trading day of the month and the last
        trading day of the month
        :param:     None
        :return:    None
        """
        # first copy the date data
        dates = self.stocks_long_term_data.index.copy(deep=True)

        # get the month data
        months = dates.month.values

        # find all the rows where the month value changes
        # note, these will all be the first trading day of the month
        month_change = np.diff(months)

        # then, get all the rows before the first trading day of the month,
        # as these will be the last trading days of the month
        shifted_backwards = shift(month_change, -1, cval=0)
        month_change += shifted_backwards

        # set the first and last rows to be the first/last trading days of the 
        # ten year period
        month_change = np.insert(month_change, 0, 1)
        month_change[-1] = 1

        # change the numeric values (1, 0, -11) to boolean values with 0 as 
        # False and all others as True
        month_change = ~(month_change == 0)

        print(month_change)
        print(len(month_change))
        print(type(month_change))

        print(self.stocks_long_term_data[month_change])


