from string import ascii_uppercase
from datetime import *
from scipy import stats
from openpyxl.chart import BarChart, Series, Reference, LineChart

import pprint
import math
import pprint

import generate_data as gd

################################################################################

# parameters that matter :)
startVal = 10
bins = 20
numberMonths = 3
savePath = "C:/Users/ericl/Desktop/"

################################################################################

# checks if the file is open
# return	True	file is closed (can save)
# return	False	fils is open (can not save)
def fileOpen(wb, fileName):
	try:
		wb.save(fileName)
		return True
	except PermissionError:
		print("ERROR: FILE IS OPEN")
		print("CLOSE FILE AND RUN SCRIPT AGAIN")
		return False

################################################################################

def save(wb):
	try:
		wb.save(savePath + "option_analysis_" + str(date.today()) + ".xlsx")
		return True
	except PermissionError:
		print("ERROR: FILE IS OPEN")
		print("CLOSE FILE AND RUN SCRIPT AGAIN")
		return False

################################################################################

# resets the sheet to default values etc.
def clean(sheet):
	for row in sheet["A1:Z70"]:
		for cell in row:
			cell.value = None
	for col in ascii_uppercase:
		sheet.column_dimensions[col].width = 12
		sheet.column_dimensions[col].hidden = False
	sheet["A1"] = "Date"
	sheet["B1"] = "Close Price"
	sheet["D" + str(startVal - 1)] = "BIN AVERAGES"
	sheet["E" + str(startVal - 1)] = "FREQUENCY"
	sheet.merge_cells("D1:E1")
	sheet["D1"] = "Statistics"
	sheet["D5"] = "60 Day Std Dev"
	sheet["D6"] = "40 Day Std Dev"
	sheet["D7"] = "20 Day Std Dev"

################################################################################

# fills in the spreadsheet with data
# return	prices	an array containing price data
def fillData(sheet):
	# does the whole date stuff
	dateCurrent = date.today()
	deltaT = timedelta(days = 90)
	dateOld = dateCurrent - deltaT
	dateCurrent = str(dateCurrent)
	dateOld = str(dateOld)

	# gets the historical data of the stock
	historicalData = gd.getHistoricalData(sheet.title, dateOld, dateCurrent)

	# puts the data into the sheet
	for row in range(0, len(historicalData)):
		sheet["A" + str(row + 2)] = historicalData[row][0]
		sheet["B" + str(row + 2)] = historicalData[row][1]

	returnArray = [0 for x in range(0, len(historicalData))];
	for i in range(0, len(historicalData)):
		returnArray[i] = historicalData[i][1]

	return returnArray

################################################################################

# fills the spreadsheet with relevant statistics
def fillStats(sheet, prices):
	try:
		# gets the basic stats from the historical data prices
		statistics = stats.describe(prices, bias=False, nan_policy="omit")
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
			sheet["D" + str(i)] = statVars[i - offset]
			sheet["E" + str(i)] = statValues[i - offset]
		sheet["D5"] = str(len(prices)) + " Day Std Dev"
		sheet["E5"] = math.sqrt(sheet["E4"].value)
		sheet["E6"] = math.sqrt(stats.describe(prices[len(prices) - 40 : len(prices)], bias=False, nan_policy="omit")[3])
		sheet["E7"] = math.sqrt(stats.describe(prices[len(prices) - 20 : len(prices)], bias=False, nan_policy="omit")[3])
	except ValueError:
		print(sheet.title + " does not exist in the free quandl database")

################################################################################

# fills the spreadsheet with relevant graphs
def graphs(sheet, prices):
	#gets the min max values of the data and computes the bin size
	try:
		minimum = stats.tmin(prices) - .1
		maximum = stats.tmax(prices) + .1
		# print("MINIMUM:           " + str(minimum))
		# print("MAXIMUM:           " + str(maximum))
		r = maximum - minimum
		deltaB = r / bins
		counts = [0] * (bins + 1)
		# print("BIN SIZE:          " + str(deltaB))

		#counts for each bin, how many fit in it
		for price in prices:
			index = int((price - minimum) / deltaB)
			# print("INDEX: ", end = "")
			# print(index)
			counts[index] += 1

		#puts the bin data into the spreadsheet
		#using D8:E28
		for i in range(startVal, startVal + bins):
			lowerBin = minimum + (deltaB * (i - 8))
			upperBin = minimum + (deltaB * (i - 7))
			binName = (upperBin + lowerBin) / 2
			# binName = i - 7
			sheet["D" + str(i)] = binName
			sheet["E" + str(i)] = counts[i - startVal]

		#generates the bar chart based on bin and frequency data
		data = BarChart()
		data.type = "col"
		data.style = 10
		data.title = sheet.title + " HISTOGRAM"
		data.x_axis_title = "BIN AVERAGE"
		data.y_axis_title = "FREQUENCY"
		foo = Reference(sheet, min_col = 5, min_row = startVal - 1, max_row = startVal + bins - 1, max_col = 5)
		cats = Reference(sheet, min_col = 4, min_row = startVal, max_row = startVal + bins - 1)
		data.add_data(foo, titles_from_data = True)
		data.set_categories(cats)
		data.shape = 4
		sheet.add_chart(data, "G4")

		#generate the linechart based on date and price
		#create chart and add data values to it
		lc = LineChart()
		lc.title = sheet.title + " LINECHART"
		lc.style = 12
		lc.y_axis_title = "PRICE"
		lc.x_axis_title = "DATE"
		lcData = Reference(sheet, min_col = 2, min_row = 1, max_row = 1 + len(prices))
		lc.add_data(lcData, titles_from_data = True)
		#style the chart
		s2 = lc.series[0]
		s2.graphicalProperties.line.solidFill = "00AAAA"
		s2.graphicalProperties.line.dashStyle = "sysDot"
		s2.graphicalProperties.line.width = 100050 # width in EMUs
		#add in the date categories
		lcDates = Reference(sheet, min_col = 1, min_row = 2, max_row = 1 + len(prices))
		lc.set_categories(lcDates)
		sheet.add_chart(lc, "G22")
	except ValueError:
		x = 1

################################################################################

def isNumber(n):
	try:
		int(n)
		return True
	except ValueError:
		return False

################################################################################

def getMonthList(currentMonth):
	returnList = [0] * numberMonths
	for i in range(1,numberMonths):
		returnList[i] = (currentMonth + i) % 12
	for i in range(0,numberMonths):
		if (returnList[i] == 0):
			returnList[i] = 12
	return returnList

################################################################################

#Creates the ten year average pages
def tenYearAverage(book):
	percSheet = book.create_sheet("10YEARAVG%", 0)
	freqSheet = book.create_sheet("10YearAVGv", 1)

	#Both of these are type ints
	thisYear = datetime.now().year
	thisMonth = datetime.now().month

	gd.formatPercOrFreqSheet(percSheet, thisYear, thisMonth)
	gd.formatPercOrFreqSheet(freqSheet, thisYear, thisMonth)

	rowNumber = 3

	for sheet in book:
		if(not isNumber(sheet.title[:1])):
			
			percentageList = [0] * 10

			gd.fillPercAndFreq(percSheet, freqSheet, thisYear, thisMonth, rowNumber, sheet.title)

			rowNumber += 1


################################################################################

