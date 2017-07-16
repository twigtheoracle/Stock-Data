from openpyxl.styles import Color, PatternFill

import numpy as np
import pprint as pp
import openpyxl
import quandl
import string
import calendar
import datetime
import time

class percentageSheet():
	# initializes the sheet with basic data
	def __init__(self, sheet, stocks):
		self.sheet = sheet
		self.stockList = stocks

		self.monthIndex = ["Jan (1)", "Feb (2)", "Mar (3)", "Apr (4)", "May (5)", "Jun (6)", "Jul (7)", "Aug (8)", "Sep (9)", "Oct (10)", "Nov (11)", "Dec (12)"]
		self.year = datetime.datetime.now().year
		self.month = datetime.datetime.now().month
		self.colorGradient=[PatternFill(start_color='E4001A', end_color='E4001A', fill_type='solid'), 
			PatternFill(start_color='E30201', end_color='E30201', fill_type='solid'), 
			PatternFill(start_color='E31c02', end_color='E31c02', fill_type='solid'), 
			PatternFill(start_color='E33602', end_color='E33602', fill_type='solid'), 
			PatternFill(start_color='E25003', end_color='E25003', fill_type='solid'), 
			PatternFill(start_color='E26904', end_color='E26904', fill_type='solid'), 
			PatternFill(start_color='E28304', end_color='E28304', fill_type='solid'), 
			PatternFill(start_color='E19C05', end_color='E19C05', fill_type='solid'), 
			PatternFill(start_color='E1B506', end_color='E1B506', fill_type='solid'), 
			PatternFill(start_color='E1CD06', end_color='E1CD06', fill_type='solid'), 
			PatternFill(start_color='DBE007', end_color='DBE007', fill_type='solid'), 
			PatternFill(start_color='C2E008', end_color='C2E008', fill_type='solid'), 
			PatternFill(start_color='A9E008', end_color='A9E008', fill_type='solid'), 
			PatternFill(start_color='91DF09', end_color='91DF09', fill_type='solid'), 
			PatternFill(start_color='79DF09', end_color='79DF09', fill_type='solid'), 
			PatternFill(start_color='60DF0A', end_color='60DF0A', fill_type='solid'), 
			PatternFill(start_color='49DE0B', end_color='49DE0B', fill_type='solid'), 
			PatternFill(start_color='31DE0B', end_color='31DE0B', fill_type='solid'), 
			PatternFill(start_color='1ADE0C', end_color='1ADE0C', fill_type='solid'), 
			PatternFill(start_color='0CDE17', end_color='0CDE17', fill_type='solid')]


	# returns a letter based on the number
	# return 	x 	a letter representation of a number (1-->A, 2-->B, ect.)
	def numberToLetter(self, n):
		num2alpha = dict(zip(range(1,27), string.ascii_uppercase))
		x = num2alpha[n]
		return x

	# formats the percentage sheet
	def formatPercentageSheet(self):

		#Puts in the months for the current month and next years months
		#Merges cells for year values
		currentYearRange = "B1:"
		nextYearRange = ""
		self.sheet["B1"] = self.year
		self.sheet["B1"].alignment = openpyxl.styles.Alignment(horizontal='center')

		numberOfMonths = 0

		index = 2
		for month in range(self.month, 13):
			self.sheet[self.numberToLetter(index) + "2"] = self.monthIndex[month - 1]
			self.sheet[self.numberToLetter(index) + "2"].alignment = openpyxl.styles.Alignment(horizontal='center')
			index += 1
			numberOfMonths += 1

		currentYearRange += self.numberToLetter(index - 1) + "1"

		index += 1

		nextYearRange += self.numberToLetter(index) + "1:"
		self.sheet[self.numberToLetter(index) + "1"] = self.year + 1
		self.sheet[self.numberToLetter(index) + "1"].alignment = openpyxl.styles.Alignment(horizontal='center')

		for month in range(1, 13):
			if (numberOfMonths == 12):
				break
			self.sheet[self.numberToLetter(index) + "2"] = self.monthIndex[month - 1]
			self.sheet[self.numberToLetter(index) + "2"].alignment = openpyxl.styles.Alignment(horizontal='center')
			index += 1
			numberOfMonths += 1

		nextYearRange += self.numberToLetter(index - 1) + "1"

		self.sheet.merge_cells(currentYearRange)
		self.sheet.merge_cells(nextYearRange)

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

	# formats the quandl query so I don't have to look at a monsterously long string :P
	# return 	returnstring 	a formatted string for quandl query
	def formatQuandlQuery(self, stock, dateOld, dateCurrent):
		returnString = ("WIKI/PRICES.json?date.gte=" + dateOld + "&date.lt=" + dateCurrent + "&ticker=" + stock + "&api_key=1qsGVmxih-dcMRsh13Zk")
		return returnString

	# probally don't need this one, but ...
	def addStock(self, index, stock):
		# comment to make this function collapse in sublime because functions need to be at least two lines to work
		self.sheet["A" + str(index)] = stock

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

		dataList = [np.mean(percentChangeList), np.std(percentChangeList, ddof = 1)]

		offset = 0
		if(booler):
			offset = 1

		self.sheet[self.numberToLetter(n + 2 + offset) + str(row + 3)] = dataList[0]

		pp.pprint(dataList)
		print()

		return [frequencyList, dataList[1]]

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

