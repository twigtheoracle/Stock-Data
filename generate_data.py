from pprint import *
from openpyxl import *
from openpyxl.styles import Alignment

import quandl
import random
import string
import calendar
import datetime
import numpy as np

################################################################################

# data :)
monthIndex = ["Jan (1)", "Feb (2)", "Mar (3)", "Apr (4)", "May (5)", "Jun (6)", "Jul (7)", "Aug (8)", "Sep (9)", "Oct (10)", "Nov (11)", "Dec (12)"]

# other import thing(s) :)
quandl.ApiConfig.api_key = "1qsGVmxih-dcMRsh13Zk"

################################################################################

def formatDate(dateString):
	returnString = ""
	for i in range(0, len(dateString)):
		if(dateString[i] != "-"):
			returnString += dateString[i]
	return returnString

################################################################################

def formatQuandlQuery(stock, startDate, endDate):
	return ("WIKI/PRICES.json?date.gte=" + startDate + "&date.lt=" + endDate + "&ticker=" + stock + "&api_key=1qsGVmxih-dcMRsh13Zk")

################################################################################

def getHistoricalData(stockName, dateOld, dateCurrent):

	dateOldFormatted = formatDate(str(dateOld))
	dateCurrentFormatted = formatDate(str(dateCurrent))

	data = quandl.get_table(formatQuandlQuery(stockName, dateOldFormatted, dateCurrentFormatted))

	length = len(data["date"])

	returnArray = [["", 0] for x in range(0, length)]
	
	for i in range(0, length):
		returnArray[i][0] = str(data["date"][i])[:10]
		returnArray[i][1] = float(data["close"][i])

	return returnArray

################################################################################

def numberToLetter(n):
	num2alpha = dict(zip(range(1,27), string.ascii_uppercase))
	return num2alpha[n]

################################################################################

def formatPercSheet(sheet, currentYear, currentMonth):

	#Puts in the months for the current month and next years months
	#Merges cells for year values
	currentYearRange = "B1:"
	nextYearRange = ""
	sheet["B1"] = currentYear
	sheet["B1"].alignment = Alignment(horizontal='center')

	numberOfMonths = 0

	index = 2
	for month in range(currentMonth, 13):
		sheet[numberToLetter(index) + "2"] = monthIndex[month - 1]
		sheet[numberToLetter(index) + "2"].alignment = Alignment(horizontal='center')
		index += 1
		numberOfMonths += 1

	currentYearRange += numberToLetter(index - 1) + "1"
	# sheet.column_dimensions[numberToLetter(index)].width = 4

	index += 1

	nextYearRange += numberToLetter(index) + "1:"
	sheet[numberToLetter(index) + "1"] = currentYear + 1
	sheet[numberToLetter(index) + "1"].alignment = Alignment(horizontal='center')

	for month in range(1, 13):
		if (numberOfMonths == 12):
			break
		sheet[numberToLetter(index) + "2"] = monthIndex[month - 1]
		sheet[numberToLetter(index) + "2"].alignment = Alignment(horizontal='center')
		index += 1
		numberOfMonths += 1

	nextYearRange += numberToLetter(index - 1) + "1"

	sheet.merge_cells(currentYearRange)
	sheet.merge_cells(nextYearRange)

################################################################################

def nextMonth(month):
	if (month == 12):
		return 1
	return month + 1

################################################################################

def nextYear(year, month):
	if (month == 12):
		return year + 1
	return year

################################################################################

def holidayExceptions(date):
	deltaT = datetime.timedelta(days = 1)

	#Beginning of month exceptions
	if (date.day < 5):
		if (date.month == 1 and date.day == 1):
			return (date + deltaT)
		if (date.month == 9 and date.weekday() == 0):
			return (date + deltaT)

	#End of month excpetions
	if (date.day > 25):
		if (date.month == 5 and date.weekday() == 0):
			return (date - datetime.timedelta(days = 3))

	return date

################################################################################

def firstValidDate(year, month):
	deltaT = datetime.timedelta(days = 1)
	date = datetime.date(year, month, 1)
	while True:
		if (date.weekday() > 4):
			date = date + deltaT
		else:
			break

	date = holidayExceptions(date)

	firstDate = str(date)
	secondDate = str(date + deltaT)

	return [firstDate, secondDate]

################################################################################

def lastValidDate(year, month):
	deltaT = datetime.timedelta(days = 1)
	date = datetime.date(year, month, calendar.monthrange(year, month)[1])
	while True:
		if (date.weekday() > 4):
			date = date - deltaT
		else:
			break

	date = holidayExceptions(date)

	firstDate = str(date)
	secondDate = str(date + deltaT)

	return [firstDate, secondDate]

################################################################################

def getMonthPercentageChange(stock, year, month):
	percentChangeList = [0.0] * 10
	frequencyList = [0, 0]
	index = 0
	for i in range(year, year - 10, -1):
		firstDays = firstValidDate(i, month)
		lastDays = lastValidDate(i, month)

		secondFirstDate = str(i) + "-" + str(month) + "-2"
		secondLastDate = str(nextYear(i, month)) + "-" + str(nextMonth(month)) + "-" + "1"

		firstDayData = quandl.get_table(formatQuandlQuery(stock, firstDays[0], firstDays[1]))
		lastDayData = quandl.get_table(formatQuandlQuery(stock, lastDays[0], lastDays[1]))

		firstDayClosePrice = firstDayData["close"][0]
		lastDayClosePrice = lastDayData["close"][0]

		percentChange = ((lastDayClosePrice - firstDayClosePrice)/firstDayClosePrice) * 100

		if(percentChange > 0):
			frequencyList[0] += 1
		else:
			frequencyList[1] += 1

		percentChangeList[index] = percentChange
		index += 1

		# print(str(i) + " " + monthIndex[month - 1] + " percentage change = " + str(percentChangeList[index - 1]))
	
	return [np.mean(percentChangeList), np.std(percentChangeList, ddof = 1), percentChangeList, frequencyList]

################################################################################

def fillPercAndFreq(percSheet, freqSheet, thisYear, thisMonth, rowNumber, stock):
	percSheet["A" + str(rowNumber)] = stock
	freqSheet["A" + str(rowNumber)] = stock

	index = 2

	for month in range (thisMonth, 13):

		PCList = getMonthPercentageChange(stock, thisYear - 1, month)

		# print("Mean: " + str(PCList[0]))
		# print("STD: " + str(PCList[1]))
		# print("FREQ: ", end = "")
		# print(PCList[3])
		# print()

		#print("MONTH: " + str(month), PCList)

		percSheet[numberToLetter(index) + str(rowNumber)] = PCList[0]
		freqSheet[numberToLetter(index) + str(rowNumber)] = str(PCList[3][0]) + ", " + str(PCList[3][1])

		printString = ""
		for i in range(0, index - 1):
			printString += ". "

		print(printString, end = "\r")

		index += 1

	print(stock + " 10 YEAR ANALYSIS COMPLETE\n")
	
################################################################################