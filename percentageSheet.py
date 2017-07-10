import numpy as np
import pprint as pp
import openpyxl
import quandl
import string
import calendar
import datetime

class percentageSheet():
	# initializes the sheet with basic data
	def __init__(self, sheet, stocks):
		self.sheet = sheet
		self.stockList = stocks

		self.monthIndex = ["Jan (1)", "Feb (2)", "Mar (3)", "Apr (4)", "May (5)", "Jun (6)", "Jul (7)", "Aug (8)", "Sep (9)", "Oct (10)", "Nov (11)", "Dec (12)"]
		self.year = datetime.datetime.now().year
		self.month = datetime.datetime.now().month

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
	# return 	string 	a formatted string for quandl query
	def formatQuandlQuery(self, stock, dateOld, dateCurrent):
		returnString = ("WIKI/PRICES.json?date.gte=" + dateOld + "&date.lt=" + dateCurrent + "&ticker=" + stock + "&api_key=1qsGVmxih-dcMRsh13Zk")
		return returnString

	def addStock(self, index, stock):
		self.sheet["A" + str(index)] = stock

	# gets a months average percentage change for a stock over the last 10 (or less) years and fills in the sheet
	# return 	frequencyList 	a list containing the frequency that the stock went up or down over the last 10 years.
	#							this is done here because repeating this function would take forever
	def fillPercentageChange(self, stock, n, row):
		# variables and such are stored in the collapsed if(True): 
		# i know, its bad
		if(True):
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

			firstDays = [datetime.date(i + yearOffset, adjustedMonth, 1), datetime.date(i + yearOffset, adjustedMonth, 2)]
			while True:
				try:
					firstDayData = quandl.get_table(self.formatQuandlQuery(stock, str(firstDays[0]), str(firstDays[1])))
					firstDayClosePrice = firstDayData["close"][0]
					if (firstDays[0].day == 6):
						break
					break
				except IndexError:
					firstDays[0] += deltaT
					firstDays[1] += deltaT

			lastDays = [datetime.date(i + yearOffset, adjustedMonth, calendar.monthrange(i + yearOffset, adjustedMonth)[1]), datetime.date(i + yearOffset, adjustedMonth, calendar.monthrange(i + yearOffset, adjustedMonth)[1]) + deltaT]
			while True:
				try:
					lastDayData = quandl.get_table(self.formatQuandlQuery(stock, str(lastDays[0]), str(lastDays[1])))
					lastDayClosePrice = lastDayData["close"][0]
					break
				except IndexError:
					lastDays[0] -= deltaT
					lastDays[1] -= deltaT		

			percentChange = ((lastDayClosePrice - firstDayClosePrice)/firstDayClosePrice) * 100

			print(i + yearOffset, adjustedMonth, percentChange)

			if(percentChange > 0):
				frequencyList[0] += 1
			else:
				frequencyList[1] += 1

			percentChangeList.append(percentChange)

		dataList = [np.mean(percentChangeList), np.std(percentChangeList, ddof = 1)]

		offset = 0
		if(booler):
			offset = 1

		self.sheet[self.numberToLetter(n + 2 + offset) + str(row + 3)] = dataList[0]

		pp.pprint(dataList)
		print()

		return frequencyList
