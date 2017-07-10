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

class stock():
	# initializes the stock with basic data
	def __init__(self, stockName, sheet, bins, savePath):
		self.stock = stockName
		self.sheet = sheet
		self.bins = bins
		self.savePath = savePath

		self.monthIndex = ["Jan (1)", "Feb (2)", "Mar (3)", "Apr (4)", "May (5)", "Jun (6)", "Jul (7)", "Aug (8)", "Sep (9)", "Oct (10)", "Nov (11)", "Dec (12)"]
		self.historicalData = []
		self.prices = []

	# formats the quandl query so I don't have to look at a monsterously long string :P
	# return 	string 	a formatted string for quandl query
	def formatQuandlQuery(self, dateOld, dateCurrent):
		returnString = ("WIKI/PRICES.json?date.gte=" + dateOld + "&date.lt=" + dateCurrent + "&ticker=" + self.stock + "&api_key=1qsGVmxih-dcMRsh13Zk")
		return returnString

	# retrieves historical data from the quandl WIKI/PRICES database between certain dates
	def getHistoricalData(self):
		dateCurrent = dt.date.today()
		dateOld = dateCurrent - dt.timeDelta(days = 90)

		dateCurrent = str(dateCurrent)
		dateOld = str(dateOld)

		data = quandl.get_table(formatQuandlQuery(dateOld, dateCurrent))

		length = len(data["date"])

		formattedDataList = [["", 0] for x in range(0, length)]
		
		for i in range(0, length):
			formattedDataList[i][0] = str(data["date"][i])[:10]
			formattedDataList[i][1] = float(data["close"][i])

		self.historicalData = []

	# fills in the spreadsheet with data
	def fillRecentData(self):
		for row in range(0, len(self.historicalData)):
			sheet["A" + str(row + 2)] = self.historicalData[row][0]
			sheet["B" + str(row + 2)] = self.historicalData[row][1]

		pricesOnlyList = [0 for x in range(0, len(self.historicalData))]

		for i in range(0, len(self.historicalData)):
			pricesOnlyList[i] = self.historicalData[i][1]

		self.prices = pricesOnlyList

	# fills the spreadsheet with relevant statistics
	def fillRecentDescriptiveStats(self):
		try:
			# gets the basic stats from the historical data prices
			statistics = stats.describe(self.prices, bias=False, nan_policy="omit")
			statVars = ["n", "x_bar", "variance", "std deviation", "skewness", "kurtosis"]
			statValues = [0,0,0,0,0]
			for i in range(0,6):
				if (i < 1):
					statValues[i] = statistics[i]
				elif (i > 1):
					statValues[i - 1] = statistics[i]

			# fill in stats to the excel worksheet
			offset = 2
			for i in range(2, 5):
				# using rows C and D for stats
				self.sheet["D" + str(i)] = statVars[i - offset]
				self.sheet["E" + str(i)] = statValues[i - offset]
			self.sheet["D5"] = str(len(self.prices)) + " Day Std Dev"
			self.sheet["E5"] = math.sqrt(self.sheet["E4"].value)
			self.sheet["E6"] = math.sqrt(stats.describe(self.prices[len(self.prices) - 40 : len(self.prices)], bias=False, nan_policy="omit")[3])
			self.sheet["E7"] = math.sqrt(stats.describe(self.prices[len(self.prices) - 20 : len(self.prices)], bias=False, nan_policy="omit")[3])
		except ValueError:
			print(self.sheet.title + " does not exist in the free quandl database")
