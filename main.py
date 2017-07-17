from pprint import pprint

import functions as f
import stock as s
import percentageSheet as ps
import frequencySheet as fs

import openpyxl
import time

start = time.time()

fileName = "template.xlsx"
bins = 20
savePath = "C:/Users/ericl/Desktop/"

wb = openpyxl.load_workbook(fileName)

run = f.fileOpen(wb, fileName, savePath)

if(run):

	# recent data
	for sheet in wb:

		print(sheet.title + " ANALYSIS")

		stock = s.stock(sheet.title, sheet, bins, savePath)
		stock.formatRecentDataSheet()
		hd = stock.getHistoricalData()
		prices = stock.fillRecentData(hd)
		stock.fillRecentDescriptiveStats(prices)
		stock.fillRecentGraphs(prices)

		print("COMPLETED\n")

	# 10 year stuff
	# percentage sheet
	stockList = wb.sheetnames
	foo = wb.create_sheet("10YR %", 0)
	percentageSheet = ps.percentageSheet(foo, stockList)

	frequencyList = []
	stdDevList = []

	percentageSheet.format()
	for i in range(0, len(stockList)):

		percentageSheet.addStock(i + 3, stockList[i])

		for monthOffset in range(0,12):

			bar, bat = percentageSheet.fillPercentageChange(stockList[i], monthOffset, i)
			frequencyList.append(bar)
			stdDevList.append(bat)

	percentageSheet.color()

	# frequency sheet
	foo = wb.create_sheet("10YR FREQ", 1)

	frequencySheet = fs.frequencySheet(foo, frequencyList, stockList)
	frequencySheet.format()
	frequencySheet.fill()
	frequencySheet.color()


	# standard deviation sheet


	#save workbook
	if (f.save(wb, savePath)):
		print("WORKBOOK COMPLETED")

timeElapsed = time.time() - start
print("\nELAPSED TIME: ", int(int(timeElapsed)/60), int(timeElapsed)%60)