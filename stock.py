from scipy import stats

import datetime as dt
import pprint as pp
import numpy as np
import openpyxl
import quandl
import string
import calendar
import sys
import math

import api_key as key

class Stock():
    # initializes the stock with basic data
    def __init__(self, sheet, data):
        self.sheet = sheet
        self.data = data
        self.data_points = len(data)
        self.data_prices = []

        self.bins = 20
        self.start_value = 10
        
    # formats the recent data sheet with column titles, etc.
    def format(self):
        # resets formatting
        # not really necessary if the template is clean
        for col in string.ascii_uppercase:
            self.sheet.column_dimensions[col].width = 12
            self.sheet.column_dimensions[col].hidden = False

        self.sheet["A1"] = "Date"
        self.sheet["B1"] = "Close Price"
        
        self.sheet.merge_cells("D1:E1")
        self.sheet["D1"] = "Statistics"
        self.sheet["D2"] = "n"
        self.sheet["D3"] = "mean"
        self.sheet["D4"] = str(self.data_points) + " Day Std Dev"
        self.sheet["D5"] = "40 Day Std Dev"
        self.sheet["D6"] = "20 Day Std Dev"

        self.sheet["D9"] = "BIN AVERAGES"
        self.sheet["E9"] = "FREQUENCY"

    # fills the sheet with data
    def fill_data(self):
        for index in range(0, self.data_points):
            self.data_prices.append(float(self.data[self.data_points - 1 - index][1]))

            self.sheet["A" + str(index + 2)] = str(self.data[self.data_points - 1 - index][0])
            self.sheet["B" + str(index + 2)] = self.data_prices[index]

    def fill_stats(self):
        statistics = stats.describe(self.data_prices, bias=False, nan_policy="omit")
        self.sheet["E2"] = statistics[0]
        self.sheet["E3"] = statistics[2]
        self.sheet["E4"] = math.sqrt(statistics[3])
        self.sheet["E5"] = math.sqrt(stats.describe(self.data_prices[self.data_points-40:], bias=False, nan_policy="omit")[3])
        self.sheet["E6"] = math.sqrt(stats.describe(self.data_prices[self.data_points-20:], bias=False, nan_policy="omit")[3])

    # def fillRecentDescriptiveStats(self, prices):
    #   # gets the basic stats from the historical data prices
    #   statistics = stats.describe(prices, bias=False, nan_policy="omit")
    #   statVars = ["n", "x_bar", "variance", "std deviation", "skewness", "kurtosis"]
    #   statValues = [0,0,0,0,0]
    #   for i in range(0,6):
    #       if (i < 1):
    #           statValues[i] = statistics[i]
    #       elif (i > 1):
    #           statValues[i - 1] = statistics[i]

    #   # fill in stats to the excel worksheet
    #   offset = 2
    #   for i in range(2, 5):
    #       # using rows C and D for stats
    #       self.sheet["D" + str(i)] = statVars[i - offset]
    #       self.sheet["E" + str(i)] = statValues[i - offset]
    #   self.sheet["D5"] = str(len(prices)) + " Day Std Dev"
    #   self.sheet["E5"] = math.sqrt(self.sheet["E4"].value)
    #   self.sheet["E6"] = math.sqrt(stats.describe(prices[len(prices) - 40 : len(prices)], bias=False, nan_policy="omit")[3])
    #   self.sheet["E7"] = math.sqrt(stats.describe(prices[len(prices) - 20 : len(prices)], bias=False, nan_policy="omit")[3])

# class Stock():
#   # initializes the stock with basic data
#   def __init__(self, stockName, sheet, bins, savePath):
#       self.stock = stockName
#       self.sheet = sheet
#       self.bins = bins
#       self.savePath = savePath

#       self.statVal = 10

#   # formats the recent data sheet with sheet titles, etc.
#   def formatRecentDataSheet(self):
#       for col in string.ascii_uppercase:
#           self.sheet.column_dimensions[col].width = 12
#           self.sheet.column_dimensions[col].hidden = False

#       self.sheet["A1"] = "Date"
#       self.sheet["B1"] = "Close Price"
        
#       self.sheet.merge_cells("D1:E1")
#       self.sheet["D1"] = "Statistics"
#       self.sheet["D5"] = "60 Day Std Dev"
#       self.sheet["D6"] = "40 Day Std Dev"
#       self.sheet["D7"] = "20 Day Std Dev"

#       self.sheet["D9"] = "BIN AVERAGES"
#       self.sheet["E9"] = "FREQUENCY"

#   # formats the quandl query so I don't have to look at a monsterously long string :P
#   # return    string  a formatted string for quandl query
#   def formatQuandlQuery(self, dateOld, dateCurrent):
#       returnString = ("WIKI/PRICES.json?date.gte=" + dateOld + "&date.lt=" + dateCurrent + "&ticker=" + self.stock + "&api_key=" + key.get_API_key())
#       return returnString

#   # retrieves historical data from the quandl WIKI/PRICES database between certain dates
#   def getHistoricalData(self):
#       dateCurrent = dt.date.today()
#       dateOld = dateCurrent - dt.timedelta(days = 90)

#       dateCurrent = str(dateCurrent)
#       dateOld = str(dateOld)

#       data = quandl.get_table(self.formatQuandlQuery(dateOld, dateCurrent))

#       length = len(data["date"])

#       formattedDataList = [["", 0] for x in range(0, length)]
        
#       for i in range(0, length):
#           formattedDataList[i][0] = str(data["date"][i])[:10]
#           formattedDataList[i][1] = float(data["close"][i])

#       return formattedDataList

#   # fills in the spreadsheet with data
#   def fillRecentData(self, hd):
#       for row in range(0, len(hd)):
#           self.sheet["A" + str(row + 2)] = hd[row][0]
#           self.sheet["B" + str(row + 2)] = hd[row][1]

#       pricesOnlyList = [0 for x in range(0, len(hd))]

#       for i in range(0, len(hd)):
#           pricesOnlyList[i] = hd[i][1]

#       return pricesOnlyList

#   # fills the spreadsheet with relevant statistics
#   def fillRecentDescriptiveStats(self, prices):
#       # gets the basic stats from the historical data prices
#       statistics = stats.describe(prices, bias=False, nan_policy="omit")
#       statVars = ["n", "x_bar", "variance", "std deviation", "skewness", "kurtosis"]
#       statValues = [0,0,0,0,0]
#       for i in range(0,6):
#           if (i < 1):
#               statValues[i] = statistics[i]
#           elif (i > 1):
#               statValues[i - 1] = statistics[i]

#       # fill in stats to the excel worksheet
#       offset = 2
#       for i in range(2, 5):
#           # using rows C and D for stats
#           self.sheet["D" + str(i)] = statVars[i - offset]
#           self.sheet["E" + str(i)] = statValues[i - offset]
#       self.sheet["D5"] = str(len(prices)) + " Day Std Dev"
#       self.sheet["E5"] = math.sqrt(self.sheet["E4"].value)
#       self.sheet["E6"] = math.sqrt(stats.describe(prices[len(prices) - 40 : len(prices)], bias=False, nan_policy="omit")[3])
#       self.sheet["E7"] = math.sqrt(stats.describe(prices[len(prices) - 20 : len(prices)], bias=False, nan_policy="omit")[3])

#   # fills the sheet with relevant graphs
#   def fillRecentGraphs(self, prices):
#       #gets the min max values of the data and computes the bin size
#       try:
#           minimum = stats.tmin(prices) - .1
#           maximum = stats.tmax(prices) + .1
#           # print("MINIMUM:           " + str(minimum))
#           # print("MAXIMUM:           " + str(maximum))
#           r = maximum - minimum
#           deltaB = r / self.bins
#           counts = [0] * (self.bins + 1)
#           # print("BIN SIZE:          " + str(deltaB))

#           #counts for each bin, how many fit in it
#           for price in prices:
#               index = int((price - minimum) / deltaB)
#               # print("INDEX: ", end = "")
#               # print(index)
#               counts[index] += 1

#           #puts the bin data into the spreadsheet
#           #using D8:E28
#           for i in range(self.statVal, self.statVal + self.bins):
#               lowerBin = minimum + (deltaB * (i - 8))
#               upperBin = minimum + (deltaB * (i - 7))
#               binName = (upperBin + lowerBin) / 2
#               # binName = i - 7
#               self.sheet["D" + str(i)] = binName
#               self.sheet["E" + str(i)] = counts[i - self.statVal]

#           #generates the bar chart based on bin and frequency data
#           data = openpyxl.chart.BarChart()
#           data.type = "col"
#           data.style = 10
#           data.title = self.stock + " HISTOGRAM"
#           data.x_axis_title = "BIN AVERAGE"
#           data.y_axis_title = "FREQUENCY"
#           foo = openpyxl.chart.Reference(self.sheet, min_col = 5, min_row = self.statVal - 1, max_row = self.statVal + self.bins - 1, max_col = 5)
#           cats = openpyxl.chart.Reference(self.sheet, min_col = 4, min_row = self.statVal, max_row = self.statVal + self.bins - 1)
#           data.add_data(foo, titles_from_data = True)
#           data.set_categories(cats)
#           data.shape = 4
#           self.sheet.add_chart(data, "G4")

#           #generate the linechart based on date and price
#           #create chart and add data values to it
#           lc = openpyxl.chart.LineChart()
#           lc.title = self.stock + " LINECHART"
#           lc.style = 12
#           lc.y_axis_title = "PRICE"
#           lc.x_axis_title = "DATE"
#           lcData = openpyxl.chart.Reference(self.sheet, min_col = 2, min_row = 1, max_row = 1 + len(prices))
#           lc.add_data(lcData, titles_from_data = True)
#           #style the chart
#           s2 = lc.series[0]
#           s2.graphicalProperties.line.solidFill = "00AAAA"
#           s2.graphicalProperties.line.dashStyle = "sysDot"
#           s2.graphicalProperties.line.width = 100050 # width in EMUs
#           #add in the date categories
#           lcDates = openpyxl.chart.Reference(self.sheet, min_col = 1, min_row = 2, max_row = 1 + len(prices))
#           lc.set_categories(lcDates)
#           self.sheet.add_chart(lc, "G22")
#       except ValueError:
#           x = 1
