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
        self.data = None
        self.data_points = None

    # verifies that a date exists and if it doesn't, goes back in time to find a date that does
    # TODO: actually write the verify date function
    def veriy_date(self, date):
        return date

    # returns stock_list as a string of the stocks delimited by commas
    def get_stock_string(self):
        return_string = ""
        for index in range(0, len(self.stock_list)):
            return_string += self.stock_list[index]
            if(index != len(self.stock_list) - 1):
                return_string += ","
        return return_string

    # gets a string that will allow me to query quandl for all the data we need
    def get_quandl_query_string(self):
        returnString = "WIKI/PRICES.json?date.gte=" + self.old_date + "&date.lt=" + self.current_date + "&ticker=" + self.get_stock_string() + "&api_key=" + key.get_API_key()
        return returnString

    # gets data from quandl and stores it in the object
    # TODO: split the data into a new dictionary with stock ticker as keys
    # TODO: make one quandl call per stock so that quandl doesn't crap itself with large tables
    def retrieve_data(self):
        self.data = quandl.get_table(self.get_quandl_query_string())
        self.data_points = len(self.data["ticker"])

    # slices self.data to return only the data of the 3 months at 20 weekdays or 30 days a month
    def get_last_3_months(self):
        # create an empty dictionary
        datatable = {}
        # iterate through every stock in the template
        for stock in self.stock_list:
            stock_data = []
            for day in range(1, 61):
                temp_date = str(self.data["date"][self.data_points - day])[:10]
                temp_price = str(self.data["close"][self.data_points - day])
                stock_data.append([temp_date, temp_price])
            datatable[stock] = stock_data
        pprint(datatable)