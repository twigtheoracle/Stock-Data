from openpyxl.styles import Color, PatternFill

import openpyxl
import datetime
import string

import apiKey

class Sheet():
	# initializes the sheet with basic data
	def __init__(self, sheet, dataList, stockList):
		self.sheet = sheet
		self.dataList = dataList
		self.stockList = stockList

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

	# formats the sheet
	def format(self):
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

		for row in range(3, 3 + len(self.stockList)):
			self.sheet["A" + str(row)] = self.stockList[row - 3]

	# fills the sheet with cool data
	def fill(self):
		index = 0
		for row in range(3, 3 + len(self.stockList)):
			for letter in range(2, 15): # from letter B to N when plugged into the first non __init__ function
				cell = self.numberToLetter(letter) + str(row)

				if (self.sheet[self.numberToLetter(letter) + "2"].value != None):

					self.sheet[cell] = self.dataList[index]

					index += 1

	# formats the quandl query so I don't have to look at a monsterously long string :P
	# return 	returnstring 	a formatted string for quandl query
	def formatQuandlQuery(self, stock, dateOld, dateCurrent):
		if(timeDelay):
			time.sleep(.5)
		returnString = ("WIKI/PRICES.json?date.gte=" + dateOld + "&date.lt=" + dateCurrent + "&ticker=" + stock + "&api_key=" + key.getAPIKey())
		return returnString
		