import datetime
import quandl

import api_key as key

class Data():
    # initializes data with the list of stocks and proper dates
    def __init__(self, stock_list):
        self.stock_list = self.get_stock_string(stock_list)
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
    def get_stock_string(self, sl):
        return_string = ""
        for index in range(0, len(sl)):
            return_string += sl[index]
            if(index != len(sl) - 1):
                return_string += ","
        return return_string

    # gets a string that will allow me to query quandl for all the data we need
    def get_quandl_query_string(self):
        returnString = "WIKI/PRICES.json?date.gte=" + self.old_date + "&date.lt=" + self.current_date + "&ticker=" + self.stock_list + "&api_key=" + key.get_API_key()
        return returnString

    # gets data from quandl and stores it in the object
    def retrieve_data(self):
        self.data = quandl.get_table(self.get_quandl_query_string())
        self.data_points = len(self.data["ticker"])
        print(self.data_points)

    # slices self.data to return only the data of the last 90 days
    def get_last_90_days(self):
        print(self.data["date"][0])
