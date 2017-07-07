from pprint import *
from openpyxl import *
from openpyxl.styles import Alignment

import quandl
import random
import string

################################################################################

# data :)
monthIndex = ["Jan (1)", "Feb (2)", "Mar (3)", "Apr (4)", "May (5)", "Jun (6)", "Jul (7)", "Aug (8)", "Sep (9)", "Oct (10)", "Nov (11)", "Dec (12)"]

################################################################################

def formatDate(dateString):
	returnString = ""
	for i in range(0, len(dateString)):
		if(dateString[i] != "-"):
			returnString += dateString[i]
	return returnString

################################################################################

def getHistoricalData(stockName, dateOld, dateCurrent):

	dateOldFormatted = formatDate(str(dateOld))
	dateCurrentFormatted = formatDate(str(dateCurrent))

	quandl.ApiConfig.api_key = "1qsGVmxih-dcMRsh13Zk"
	data = quandl.get_table("WIKI/PRICES.json?date.gte=" + dateOldFormatted + "&date.lt=" + dateCurrentFormatted + "&ticker=" + stockName + "&api_key=1qsGVmxih-dcMRsh13Zk")

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

def formatPercOrFreqSheet(sheet, currentYear, currentMonth):

	#Puts in the months for the current month and next years months
	#Merges cells for year values
	currentYearRange = "B1:"
	nextYearRange = ""
	sheet["B1"] = currentYear
	sheet["B1"].alignment = Alignment(horizontal='center')

	index = 2
	for month in range(currentMonth, 13):
		sheet[numberToLetter(index) + "2"] = monthIndex[month - 1]
		sheet[numberToLetter(index) + "2"].alignment = Alignment(horizontal='center')
		index += 1

	currentYearRange += numberToLetter(index - 1) + "1"
	# sheet.column_dimensions[numberToLetter(index)].width = 4

	index += 1

	nextYearRange += numberToLetter(index) + "1:"
	sheet[numberToLetter(index) + "1"] = currentYear + 1
	sheet[numberToLetter(index) + "1"].alignment = Alignment(horizontal='center')

	for month in range(1, 13):
		sheet[numberToLetter(index) + "2"] = monthIndex[month - 1]
		sheet[numberToLetter(index) + "2"].alignment = Alignment(horizontal='center')
		index += 1

	nextYearRange += numberToLetter(index - 1) + "1"

	sheet.merge_cells(currentYearRange)
	sheet.merge_cells(nextYearRange)

################################################################################

def fillPercAndFreq(percSheet, freqSheet, thisYear, thisMonth, rowNumber, stockName):
	percSheet["A" + str(rowNumber)] = stockName
	freqSheet["A" + str(rowNumber)] = stockName
	

