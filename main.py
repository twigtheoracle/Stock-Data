from pprint import pprint

import openpyxl
import time

import functions as f
import stock as s
import percentageSheet as ps
import frequencySheet as fs
import stdevSheet as sds

try:
	start = time.time()

	fileName = "test_template.xlsx"
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


		# standard deviation sheet
		foo = wb.create_sheet("10YR % STD Dev", 1)

		stdevSheet = sds.stdevSheet(foo, stdDevList, stockList)
		stdevSheet.format()
		stdevSheet.fill()
		stdevSheet.color()


		# frequency sheet
		foo = wb.create_sheet("10YR FREQ", 2)

		frequencySheet = fs.frequencySheet(foo, frequencyList, stockList)
		frequencySheet.format()
		frequencySheet.fill()
		frequencySheet.color()

		#save workbook
		if (f.save(wb, savePath)):
			print("WORKBOOK COMPLETED")

	timeElapsed = time.time() - start
	# im not sure if time will automatically cast to an int and im too lazy to look it up :D
	print("\nELAPSED TIME:", str(int(int(timeElapsed)/60)) + "m", str(int(timeElapsed)%60)+"s")

except quandl.errors.quandl_error.QuandlError:
	print("504: GATEWAY TIMEOUT ERROR")
	print("TRY TO RUN THE PROGRAM AGAIN")