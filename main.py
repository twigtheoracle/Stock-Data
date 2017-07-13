import openpyxl

import functions as f
import stock as s
import percentageSheet as ps

fileName = "test_template.xlsx"
bins = 20
savePath = "C:/Users/ericl/Desktop/"

wb = openpyxl.load_workbook(fileName)

run = f.fileOpen(wb, fileName, savePath)

if(run):

	#iterate through the sheets
	# for sheet in wb:

	# 	print(sheet.title + " ANALYSIS")

	# 	stock = s.stock(sheet.title, sheet, bins, savePath)

	# 	stock.formatRecentDataSheet()

	# 	hd = stock.getHistoricalData()

	# 	prices = stock.fillRecentData(hd)

	# 	stock.fillRecentDescriptiveStats(prices)

	# 	stock.fillRecentGraphs(prices)

	# 	print("COMPLETED\n")

	stockList = wb.sheetnames

	foo = wb.create_sheet("10YR %", 0)

	percentageSheet = ps.percentageSheet(foo, stockList)

	percentageSheet.formatPercentageSheet()

	for i in range(0, len(stockList)):

		percentageSheet.addStock(i + 3, stockList[i])

		for monthOffset in range(0,12):

			percentageSheet.fillPercentageChange(stockList[i], monthOffset, i)

	#save workbook
	if (f.save(wb, savePath)):
		print("WORKBOOK COMPLETED")