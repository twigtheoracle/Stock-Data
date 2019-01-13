from pprint import *
from calendar import monthrange
from tqdm import tqdm

import datetime
import quandl
import numpy as np

import urllib.request, json # for getting data from AV

import api_key as key

class Data():
    # initializes data with the list of stocks and proper dates
    def __init__(self, sl):
        self.stock_list = sl

        self.current_date = str(datetime.date.today())
        self.current_year = int(self.current_date[:4])
        self.current_month = int(self.current_date[5:7])
        self.old_date = self.get_old_date(self.current_date)
        self.old_year = int(self.old_date[:4])
        self.data = {}

        # initialize quandl with the api key
        quandl.ApiConfig.api_key = key.get_Quandl_API_key()

    # gets the old date for data access
    def get_old_date(self, date):
        return_string = ""
        return_string += str(self.current_year - 11) + "-"
        if(self.current_month < 10):
            return_string += "0"
        return_string += str(self.current_month) + "-01"
        return return_string

    # gets a string that will allow me to query quandl for all the data we need
    def get_quandl_query_string(self, stock):
        return_string = "EOD&json?date.gte=" + self.old_date + "&date.lt=" + self.current_date + "&ticker=" + stock + "&api_key=" + key.get_Quandl_API_key()
        return return_string

    # gets a string that will allow me to query Alpha Vantage for data needed
    def get_AV_query_string(self, stock):
        return_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + stock + "&outputsize=full&apikey=" + key.get_AV_API_key()
        return return_string

    # gets data from a data provier and stores it in the object
    def retrieve_data(self, data_provider = "Quandl"):
        # data must be formatted as such:
        # * means the data is used in processing
        # note that all structures in data: are lists and not dictonaries
        # note that data is organized with furthest back in time at index zero and most recent data at the last index
        # datatable:
        #   stock:
        #       data:
        #           ticker: (single value)
        #           date: * (numpy string array)
        #           adj_close: * (numpy float array)
        print("getting stock information...")
        for stock in tqdm(self.stock_list):
            stock_data = {}
            formatted_data = None
            if(data_provider == "Quandl"):
                quandl_data = quandl.get("EOD/" + stock, start_date = self.old_date, end_date = self.current_date)
                # print(quandl_data)
                stock_data["data_length"] = len(quandl_data["Open"])
                # Current format is:
                # datatable:
                #   Meta Data:
                #       1. Information:
                #       2. Symbol:
                #       3. Last Refreshed:
                #       4. Output Size:
                #       5. Time Zone:
                #   Data:
                #       Open:
                #           Date: Value
                #           Date: Value
                #           etc...
                #       Close:
                #           Date: Value
                #           Date: Value
                #           etc...
                #       etc...

                # format the data properly
                # we only care about the ticker, date, and adjusted closing price
                # note: "U10" means string of length 10, thats just how np.empty works
                formatted_data = {"ticker": stock, 
                                  "date": np.empty(stock_data["data_length"], dtype="U10"), 
                                  "adj_close": np.empty(stock_data["data_length"])
                                  }
                # get a list of the dates and iterate over them
                date_keys = quandl_data["Open"].keys()
                for index in range(0, stock_data["data_length"]):
                    formatted_data["date"][index] = str(date_keys[index])[:11]
                    formatted_data["adj_close"][index] = quandl_data["Adj_Close"][date_keys[index]] 

            stock_data["data"] = formatted_data

            self.data[stock] = stock_data

    # slices self.data to return only the data of the last 3 months (every month has 4 weeks and 5 weekdays a week, so there are 20 days a month and 60 days for 3 months)
    def get_short_term_data(self):
        # create an empty dictionary
        datatable = {}
        # iterate through every stock in the template
        try:
            for stock in self.stock_list:
                stock_data = []
                for day in range(1, 61):
                    temp_date = str(self.data[stock]["data"]["date"][self.data[stock]["data_length"] - day])[:10]
                    temp_price = str(self.data[stock]["data"]["adj_close"][self.data[stock]["data_length"] - day])
                    stock_data.append([temp_date, temp_price])
                datatable[stock] = stock_data
        except IndexError:
            print("INDEXERROR")
        except KeyError:
            print("KEYERROR: Stock is newer than three months")

        return datatable

    # returns the percentage change of the given month in the given year of the given stock
    def get_percentage_change(self, stock_name, year, month):

        first_month = str(self.data[stock_name]["data"]["date"][0])[5:7]
        first_year = str(self.data[stock_name]["data"]["date"][0])[:4]

        # if data does not exist, return None
        if(int(first_year) > year or (int(first_year) == year and int(first_month) > month)):
            print("DATA DOES NOT EXIST:", first_year + "-" + first_month, str(year) + "-" + str(month))
            return None

        years_since_start = year - int(first_year)
        months_since_start = month - int(first_month)

        # every year has 252 trading days on average and every month has 21 trading days on average 
        # these indicies are approximate values
        month_start_index = (years_since_start * 252) + (months_since_start * 21)
        month_end_index = (years_since_start * 252) + (months_since_start * 21) + 21

        percentage_change = None

        try:
            # this turns the indicies into the true values
            while(True):
                if(month_start_index < 0 or int(str(self.data[stock_name]["data"]["date"][month_start_index])[5:7]) != month):
                    month_start_index += 1
                    break
                month_start_index -= 1
            while(True):
                if(month_end_index < 0 or int(str(self.data[stock_name]["data"]["date"][month_end_index])[5:7]) == month):
                    break
                month_end_index -= 1

            percentage_change = (self.data[stock_name]["data"]["adj_close"][month_end_index] - self.data[stock_name]["data"]["adj_close"][month_start_index]) / self.data[stock_name]["data"]["adj_close"][month_start_index]

            print(stock_name, year, month, percentage_change)

        except KeyError:
            print("KEYERROR: " + stock_name + " did not exist at " + str(year) + "-" + str(month))
            pass

        # print(year, month, "(" + str(self.data[stock_name]["data"]["date"][month_start_index])[:10] + ", " + str(self.data[stock_name]["data"]["close"][month_start_index]) + ")", "(" + str(self.data[stock_name]["data"]["date"][month_end_index])[:10] + ", " + str(self.data[stock_name]["data"]["close"][month_end_index]) + ")")

        # print(year, month, str(self.data[stock_name]["data"]["date"][month_start_index])[:10], self.data[stock_name]["data"]["close"][month_start_index], str(self.data[stock_name]["data"]["date"][month_end_index])[:10], self.data[stock_name]["data"]["close"][month_end_index])

        return percentage_change

    # gets the average percent change of a month for a specific stock
    # returns a datalist constructed: [average percent change, std dev of percent change, frequency positive percent change]
    def get_average_percent_change(self, stock_name, month):
        year_offset = None
        # for the current month and all months after it, we need to look at data up to last year
        if(month >= self.current_month):
            year_offset = 1
        else:
            year_offset = 0

        datalist = []
        for year in range(self.current_year - 10 - year_offset, self.current_year - year_offset):
            # TODO: get_percentage_change returns None for change
            change = self.get_percentage_change(stock_name, year, month)
            # print(year, month, change)
            if(change != None):
                datalist.append(change)

        return_data = None
        try:
            count = 0
            for data_point in datalist:
                if(data_point > 0):
                    count += 1
            percent_positive = (count / len(datalist)) * 100

            return_data = [np.mean(datalist) * 100, np.std(datalist), percent_positive]
        # this error occurs when there is not enough data to do standard deviation
        except ZeroDivisionError:
            print("WARNING: DIVIDE BY ZERO ERROR")
            return_data = [None, None, None]

        # print(stock_name, month, datalist, "\n")

        return return_data
        
    # returns a datatable with all long term data for every single stock
    def get_long_term_data(self):
        # datatable:
        #   percent_change:
        #       stock:
        #           data...
        #       stock:
        #           data...
        #   std_dev:    
        #       etc...
        datatable = {}
        datatable["percent_change"] = {}
        datatable["std_dev"] = {}
        datatable["freq"] = {}
        datatable["years"] = {}
        print("\ngetting long term data...")
        # for stock in tqdm(self.stock_list):
        for stock in self.stock_list:
            datatable["percent_change"][stock] = []
            datatable["std_dev"][stock] = []
            datatable["freq"][stock] = []
            datatable["years"][stock] = int(self.data[stock]["data_length"] / 252) + 1
            for month in range(self.current_month - 1, self.current_month - 1 + 12):
                adjusted_month = (month % 12) + 1
                datalist = self.get_average_percent_change(stock, adjusted_month)
                datatable["percent_change"][stock].append(datalist[0])
                datatable["std_dev"][stock].append(datalist[1])
                datatable["freq"][stock].append(datalist[2])
                if(adjusted_month - self.current_month == 3):
                    four_month_percentage_change = 1
                    for back_data in range(-1, -5, -1):
                        # print(datatable["percent_change"][stock][back_data], (1 + (datatable["percent_change"][stock][back_data] / 100)))
                        four_month_percentage_change *= (1 + (datatable["percent_change"][stock][back_data] / 100))

                    p_consec_4_pos = 1
                    for back_data in range(-1, -5, -1):
                        # print(datatable["percent_change"][stock][back_data], (1 + (datatable["percent_change"][stock][back_data] / 100)))
                        p_consec_4_pos *= ((datatable["freq"][stock][back_data] / 100))
                    # print("")

                    datatable["percent_change"][stock].append(four_month_percentage_change * 100 - 100)
                    datatable["std_dev"][stock].append(None)
                    datatable["freq"][stock].append(p_consec_4_pos * 100)
                if(adjusted_month == 12):
                    datatable["percent_change"][stock].append(None)
                    datatable["std_dev"][stock].append(None)
                    datatable["freq"][stock].append(None)
        print("done")
        return datatable

