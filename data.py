from pprint import *
from calendar import monthrange

import datetime
import quandl

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

    # gets the old date for data access
    def get_old_date(self, date):
        return_string = ""
        return_string += str(self.current_year - 10) + "-"
        if(self.current_month < 10):
            return_string += "0"
        return_string += str(self.current_month) + "-01"
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

    # slices self.data to return only the data of the last 3 months (every month has 4 weeks and 5 weekdays a week, so there are 20 days a month and 60 days for 3 months)
    def get_last_3_months(self):
        # create an empty dictionary
        datatable = {}
        # iterate through every stock in the template
        try:
            for stock in self.stock_list:
                stock_data = []
                for day in range(1, 61):
                    temp_date = str(self.data[stock]["data"]["date"][self.data[stock]["data_length"] - day])[:10]
                    temp_price = str(self.data[stock]["data"]["close"][self.data[stock]["data_length"] - day])
                    stock_data.append([temp_date, temp_price])
                datatable[stock] = stock_data
        except IndexError:
            print("INDEXERROR")

        return datatable

    # gets the percentage change of the given month in the given year of the given stock
    def get_percentage_change(self, stock_name, year, month):
        years_since_start = year - self.old_year
        months_since_start = month - self.current_month

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

            percentage_change = (self.data[stock_name]["data"]["close"][month_end_index] - self.data[stock_name]["data"]["close"][month_start_index]) / self.data[stock_name]["data"]["close"][month_start_index]

        except KeyError:
            print("KEYERROR:", stock_name, year, month, month_start_index, month_end_index)

        return percentage_change

    def get_average_percent_change(self, stock_name, month):
        year_offset = None
        # for the current month and all months after it, we need to look at data up to last year
        if(month >= self.current_month):
            year_offset = 1
        else:
            year_offset = 0

        datalist = []
        for year in range(self.current_year - 10 - year_offset, self.current_year - year_offset):
            datalist.append(self.get_percentage_change(stock_name, year, month))
        print(stock_name, datalist, "")
        

