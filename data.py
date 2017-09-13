import datetime
import quandl

import api_key as key

class Data():
    # initializes data with the list of stocks and proper dates
    def __init__(self, stock_list):
        self.stock_list = stock_list
        current_date = str(datetime.date.today())
        #TODO: verify that old_date will exist (think leap years)
        old_date = str(int(current_date[:4]) - 10) + current_date[4:]
        self.current_date = current_date
        self.old_date = self.veriy_date(old_date)
        self.data = None

    # verifies that a date exists and if it doesn't, goes back in time to find a date that does
    def veriy_date(self, date):
        pass

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
        returnString = ("WIKI/PRICES.json?date.gte=" + self.old_date + "&date.lt=" + self.current_date + "&ticker=" + self.get_stock_string + "&api_key=" + key.getAPIKey())
        return returnString

    # gets data from quandl and stores it in the object
    def get_data(self):
        self.data = quandl.get_table(self.get_quandl_query_string())
