from openpyxl.styles import Color, PatternFill

import numpy as np
import pprint as pp
import openpyxl
import quandl
import string
import calendar
import datetime
import time
import math

import apiKey as key
import sheet

class percentageSheet(sheet.Sheet):
	# a silly function, i'm sure there's some library out there that will do this for me
	# return 	1 			if the month is twelve (Dec), the next month is 1 (Jan)
	# return 	month + 1	if the month is not twelve, the next month is month + 1
	def nextMonth(self, month):
		if (month == 12):
			return 1
		return month + 1

	# look above :D
	# return 	year + 1	if the month is twelve, the year increments by one
	# return  	year 		if the month is not twelve, the year remains the same
	def nextYear(self, year, month):
		if (month == 12):
			return year + 1
		return year

	# returns the percentage change of a stock based on year and month
	# return 	percentageChange 	the percentage change of that year and month
	def getPercentageChange(self, stock, year, month):
		monthStartPrice = -1
		monthEndPrice = -1

		firstDay = datetime.date(year, month, 1)
		lastDay = datetime.date(year, month, calendar.monthrange(year, month)[1])

		data = quandl.get_table(self.formatQuandlQuery(stock, str(firstDay), str(lastDay)))

		index = 0
		while True:
			try:
				if (index >= 6):
					return None
				monthStartPrice = data["close"][index]
				break
			except IndexError:
				index += 1

		index = len(data["close"]) - 1
		while True:
			try:
				if (index == -1):
					return None
				monthEndPrice = data["close"][index]
				break
			except IndexError:
				index -= 1

		# if we are looking too far back in time for prices to exist
		if (monthStartPrice == -1 or monthEndPrice == -1):
			return None

		return ((monthEndPrice - monthStartPrice)/monthStartPrice) * 100

	# gets a months percentage change and fills it into the percentage sheet
	# return 	frequencyList 	a list containing the frequency that the stock went up or down over the last 10 years.
	#							this is done here because repeating this function would take forever
	def fillPercentageChange(self, stock, n, row):
		percentChangeList = []
		frequencyList = [0, 0]
		deltaT = datetime.timedelta(days = 1)

		yearOffset = 0

		firstDays = None
		firstDayData = None
		firstDayClosePrice = None

		lastDays = None
		lastDayData = None
		lastDayClosePrice = None

		adjustedMonth = n + self.month
		booler = False
		if(adjustedMonth >= 13):
			booler = True
			adjustedMonth -= 12

		for i in range(self.year - 1, self.year - 11, -1):

			if(adjustedMonth < self.month):
				yearOffset = 1

			percentageChange = self.getPercentageChange(stock, i + yearOffset, adjustedMonth)

			print(stock, i + yearOffset, adjustedMonth, percentageChange)

			if (percentageChange != None):
				percentChangeList.append(percentageChange)
				if(percentageChange > 0):
					frequencyList[0] += 1
				elif(percentageChange < 0):
					frequencyList[1] += 1
			else:
				break

		dataList = [np.mean(percentChangeList), np.std(percentChangeList, ddof = 1)]

		if(math.isnan(dataList[1])):
			dataList[1] = None

		offset = 0
		if(booler):
			offset = 1

		self.sheet[self.numberToLetter(n + 2 + offset) + str(row + 3)] = round(dataList[0], 2)

		pp.pprint(dataList)
		print()

		up = frequencyList[0]
		down = frequencyList[1]

		percentUp = round((up*100)/(up + down), 2)

		return (percentUp, dataList[1])

	# colors each numerical percentage a color based on a pretty gradient from red to green
	def color(self):
		for letter in range(2, 15): # from letter B to N when plugged into the first non __init__ function
			for row in range(3, 3 + len(self.stockList)):
				cell = self.numberToLetter(letter) + str(row)
				value = self.sheet[cell].value

				if (value != None):
					value = int(value + 10)
					if (value <= 0):
						value = 0
					elif (value >= 19):
						value = 19
					self.sheet[cell].fill = self.colorGradient[value]

	# overrides Sheet.fill(self)
	def fill(self, frequencyList, stdevList):
		for i in range(0, len(self.stockList)):
			for monthOffset in range(0,12):

				bar, bat = self.fillPercentageChange(self.stockList[i], monthOffset, i)
				frequencyList.append(bar)
				stdevList.append(bat)