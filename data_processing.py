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

        # create the dataframe to hold the recent summary statistics
        self.summary_statistics = pd.DataFrame(index=sl)

        # create a dictionary to hold the binning data
        self.bins = {}

        # create the dataframe to hold the average monthly change data
        self.monthly_change_data = pd.DataFrame(index=sl)

        # create the dataframe to hold the positive frequency of monthy change
        self.monthly_frequency_data = pd.DataFrame(index=sl)

        # create the dataframe to hold the frequency data
        self.frequency_data = pd.DataFrame()

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
        short_term_data_start = datetime.date(today.year, today.month - 3, 
            today.day)

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

    def compute_summary_statistics(self):
        """
        Computes the short term summary statistics of all the stocks. These 
        include number of data points (63), mean, three month std (63 days), 
        two month std (42 days), and one month std (21 days). This function also
        bins the data to make the histogram creation easier
        Note, 21 trading days approximates one month, according to Wikipedia
        :param:     None
        :return:    None
        """
        # add the count column
        self.summary_statistics["n"] = \
            [63 for i in range(0, len(self.stock_list))]

        # add the mean column
        self.summary_statistics["mean"] = self.stocks_short_term_data.mean()

        # add teh std columns
        self.summary_statistics["3 month std"] = \
            self.stocks_short_term_data.std()
        self.summary_statistics["2 month std"] = \
            self.stocks_short_term_data[21:].std()
        self.summary_statistics["1 month std"] = \
            self.stocks_short_term_data[42:].std()
        # compute the bins for each column
        for stock in self.stock_list:
            # compute which of 20 intervals each recent data point falls into
            stock_intervals = pd.cut(self.stocks_short_term_data[stock], 
                bins=20)

            # count and store each interval
            self.bins[stock] = stock_intervals.value_counts(sort=False)

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

        # select only the rows of self.stocks_long_term_data where the month is
        # changing
        self.stocks_long_term_data = self.stocks_long_term_data[month_change]

    def get_monthly_percent_change(self):
        """
        Computes the percent change for each month for each stock given the 
        cut daily data. Modifies self.stocks_long_term_data to hold the
        average monthly change for the stocks
        :param:     None
        :return:    None
        """
        # first, change the datetime index to a multiindex with the levels
        # year and month
        self.stocks_long_term_data.index = pd.MultiIndex.from_arrays([
            self.stocks_long_term_data.index.year,
            self.stocks_long_term_data.index.month])
        self.stocks_long_term_data.index.names = ["Year", "Month"]

        # get the monthly change for the stocks
        change = self.stocks_long_term_data.diff()

        # get the percent change for the stocks
        # select only the rows that we care about: 
        # from the change df, we only want the end of the month diff rows, since
        # that value is the end of the month minus the beginning of the month
        # from the long term data df, we only want the beginning of the month
        # rows since that is what the change should be compared to
        change = change.iloc[1::2]
        self.stocks_long_term_data = self.stocks_long_term_data.iloc[::2]

        # divide the change by the baseline to get the percent change
        percent_change = change / self.stocks_long_term_data
        percent_change *= 100

        # save the percent_change in the long term data df
        self.stocks_long_term_data = percent_change

    def compute_monthly_change(self):
        """
        Computes the average monthly change for a particular stock for as much 
        data as exists. Does this for all months and all stocks
        :param:     None
        :return:    None
        """
        # iterate over all the months starting from the month where our monthly
        # data ends (self.dates[2].month)
        for month in range(self.dates[2].month, self.dates[2].month + 12):
            # adjust the month to be the the range 1-12
            adj_month = (month % 12) + 1

            # select the rows of the where the month equals the current 
            # iteration
            month_data = \
                self.stocks_long_term_data[\
                self.stocks_long_term_data.index.get_level_values("Month") == \
                adj_month]

            # get the average for each month
            month_data = month_data.mean(axis=0)

            # add the data as a row in the monthly change df
            self.monthly_change_data[adj_month] = month_data

    def compute_monthly_frequency(self):
        """
        Computes the chance of a particular stock going up during a month, 
        based on historical data as calculated by get_monthly_percent_change().
        Does this for all months and all stocks
        :param:     None
        :return:    None
        """
        # iterate over all the months starting from the month where our monthly
        # data ends (self.dates[2].month)
        for month in range(self.dates[2].month, self.dates[2].month + 12):
            # adjust the month to be in the range 1-12
            adj_month = (month % 12) + 1

            # select the rows of the table where the month equals the current 
            # adjusted month
            month_data = \
                self.stocks_long_term_data[\
                self.stocks_long_term_data.index.get_level_values("Month") == \
                adj_month]

            # count the number of non-NaN in each column
            num_data_points = month_data.count()

            # fill missing data with 0
            month_data = month_data.fillna(0)

            # change all data points greater than 0 to 1
            month_data = ((month_data > 0) * 1)

            # count the number of years where this particular month had a 
            # postiive gain
            month_data = month_data.sum()

            # get the frequency of positive change and store it in the df
            month_data = month_data / num_data_points
            self.monthly_frequency_data[adj_month] = month_data
