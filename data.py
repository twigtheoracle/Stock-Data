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

    # returns stock_list as a string of the stocks delimited by commas
    def get_stock_string(self):
        return_string = ""
        for index in range(0, len(self.stock_list)):
            return_string += self.stock_list[index]
            if(index != len(self.stock_list) - 1):
                return_string += ","
        return return_string

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

    # slices self.data to return only the data of the 3 months at 20 weekdays or 30 days a month
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
        pprint(datatable)
        return datatable