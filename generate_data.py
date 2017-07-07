from pprint import *

import quandl
import random

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

def fillPercentageAndFreq(percSheet, freqSheet, year, monthList, row, stockName):
	percSheet["A" + str(row)] = stockName + " percentages go here"
	freqSheet["A" + str(row)] = stockName + " frequencies go here"
