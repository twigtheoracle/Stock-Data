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

    # fills the sheet with recent descriptive stats(n, mean, standard deviations for different time periods)
    def fill_stats(self):
        statistics = stats.describe(self.data_prices, bias=False, nan_policy="omit")
        self.sheet["E2"] = statistics[0]
        self.sheet["E3"] = statistics[2]
        self.sheet["E4"] = math.sqrt(statistics[3])
        self.sheet["E5"] = math.sqrt(stats.describe(self.data_prices[self.data_points-40:], bias=False, nan_policy="omit")[3])
        self.sheet["E6"] = math.sqrt(stats.describe(self.data_prices[self.data_points-20:], bias=False, nan_policy="omit")[3])

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
