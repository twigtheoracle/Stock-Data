from pprint import *

import datetime
import quandl

import api_key as key

class Data():
    # initializes data with the list of stocks and proper dates
    def __init__(self, sl):
        self.stock_list = sl
        cd = str(datetime.date.today())
        od = str(int(cd[:4]) - 10) + cd[4:]
        self.current_date = cd
        self.old_date = self.veriy_date(od)
        self.data = {}

    # verifies that a date exists and if it doesn't, goes back in time to find a date that does
    # TODO: actually write the verify date function
    def veriy_date(self, date):
        return date

    # gets a string that will allow me to query quandl for all the data we need
    def get_quandl_query_string(self, stock):
        returnString = "WIKI/PRICES.json?date.gte=" + self.old_date + "&date.lt=" + self.current_date + "&ticker=" + stock + "&api_key=" + key.get_API_key()
        return returnString

    # gets data from quandl and stores it in the object
    def retrieve_data(self):
        for stock in self.stock_list:
            temp_data = {}
            temp_quandl_data = quandl.get_table(self.get_quandl_query_string(stock))
            temp_data["data"] = temp_quandl_data
            temp_data["data_length"] = len(temp_quandl_data["ticker"])

            self.data[stock] = temp_data

    # slices self.data to return only the data of the last 3 months (every month has 4 weeks and 5 weekdays a week, so there are 20 days a month and 60 days for 3 months)
    def get_last_3_months(self):
        # create an empty dictionary
        datatable = {}
        # iterate through every stock in the template
        for stock in self.stock_list:
            stock_data = []
            for day in range(1, 61):
                temp_date = str(self.data[stock]["data"]["date"][self.data[stock]["data_length"] - day])[:10]
                temp_price = str(self.data[stock]["data"]["close"][self.data[stock]["data_length"] - day])
                stock_data.append([temp_date, temp_price])
            datatable[stock] = stock_data
        return datatable

    # TODO: write this damn function
    def get_percentage_change(self, stock_name, year, month):
        pass