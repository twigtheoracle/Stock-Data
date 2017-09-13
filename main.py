from pprint import pprint

import openpyxl
import time
import quandl

import functions as f
import stock as s

from data import *

import classes

start = time.time

data = Data(["AAPL", "GOOGL", "ACN"])
data.retrieve_data()
short_term_data = data.get_last_3_months()

# try:
#
# 	fileName = "template.xlsx"
# 	bins = 20
# 	savePath = "C:/Users/ericl/Desktop/"
#
# 	wb = openpyxl.load_workbook(fileName)
#
# 	run = f.fileOpen(wb, fileName, savePath)
#
# 	if(run):
#
# 		# recent data
# 		for sheet in wb:
#
# 			print(sheet.title + " ANALYSIS")
#
# 			stock = s.Stock(sheet.title, sheet, bins, savePath)
# 			stock.formatRecentDataSheet()
# 			hd = stock.getHistoricalData()
# 			prices = stock.fillRecentData(hd)
# 			stock.fillRecentDescriptiveStats(prices)
# 			stock.fillRecentGraphs(prices)
#
# 			print("COMPLETED\n")
#
# 		# 10 year stuff
# 		stockList = wb.sheetnames
# 		frequencyList = []
# 		stdevList = []
#
#
# 		# percentage sheet
# 		foo = wb.create_sheet("10YR %", 0)
#
# 		percentageSheet = classes.PercentageSheet(foo, [], stockList)
# 		percentageSheet.format()
# 		monthMeans = percentageSheet.fill(frequencyList, stdevList)
# 		percentageSheet.color()
#
#
# 		# standard deviation sheet
# 		foo = wb.create_sheet("10YR % STD Dev", 1)
#
# 		#TODO: use monthMeans to switch std dev coloring to being percentage based
# 		stdevSheet = classes.StdevSheet(foo, stdevList, stockList)
# 		stdevSheet.format()
# 		stdevSheet.fill()
# 		stdevSheet.color()
#
#
# 		# frequency sheet
# 		foo = wb.create_sheet("10YR FREQ", 2)
#
# 		frequencySheet = classes.FrequencySheet(foo, frequencyList, stockList)
# 		frequencySheet.format()
# 		frequencySheet.fill()
# 		frequencySheet.color()
#
# 		#save workbook
# 		if (f.save(wb, savePath)):
# 			print("WORKBOOK COMPLETED")
#
# 		timeElapsed = time.time() - start
# 		# im not sure if time will automatically cast to an int and im too lazy to look it up :D
# 		print("\nELAPSED TIME:", str(int(int(timeElapsed)/60)) + "m", str(int(timeElapsed)%60)+"s")
#
# except quandl.errors.quandl_error.QuandlError:
# 	if (f.save(wb, savePath)):
# 		print("INCOMPLETE WORKBOOK SAVED")
# 	print("===PROGRAM TERMINATED===\n")
# 	timeElapsed = time.time() - start
# 	# im not sure if time will automatically cast to an int and im too lazy to look it up :D
# 	print("\nELAPSED TIME:", str(int(int(timeElapsed)/60)) + "m", str(int(timeElapsed)%60)+"s")
# 	print("504: GATEWAY TIMEOUT ERROR")
# 	print("TRY TO RUN THE PROGRAM AGAIN")
#
# except KeyboardInterrupt:
# 	if (f.save(wb, savePath)):
# 		print("\n\nINCOMPLETE WORKBOOK SAVED")
# 	print("===PROGRAM TERMINATED===")
# 	print("KEYBOARD INTERRUPT\n")
# 	timeElapsed = time.time() - start
# 	# im not sure if time will automatically cast to an int and im too lazy to look it up :D
# 	print("\nELAPSED TIME:", str(int(int(timeElapsed)/60)) + "m", str(int(timeElapsed)%60)+"s")
#
# except ConnectionResetError:
# 	if (f.save(wb, savePath)):
# 		print("\n\nINCOMPLETE WORKBOOK SAVED")
# 	print("===PROGRAM TERMINATED===\n")
# 	print("CONNECTION RESET ERROR\n")
# 	timeElapsed = time.time() - start
# 	# im not sure if time will automatically cast to an int and im too lazy to look it up :D
# 	print("\nELAPSED TIME:", str(int(int(timeElapsed)/60)) + "m", str(int(timeElapsed)%60)+"s")
