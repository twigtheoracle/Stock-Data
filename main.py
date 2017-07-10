import openpyxl

import functions as f
import stock as s

fileName = "test_template.xlsx"
bins = 20
savePath = "C:/Users/ericl/Downloads/"

wb = openpyxl.load_workbook(fileName)

run = f.fileOpen(wb, fileName)

if(run):

	#iterate through the sheets
	for sheet in wb:

		stock = s.stock(sheet.title, sheet, bins, savePath)

		stock.formatRecentDataSheet()

		hd = stock.getHistoricalData()

		prices = stock.fillRecentData(hd)

		stock.fillRecentDescriptiveStats(prices)

		stock.fillRecentGraphs(prices)

	# f.tenYearAverage(wb)

	#save workbook
	if (f.save(wb)):
		print("WORKBOOK COMPLETED")