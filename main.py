from pprint import pprint

import openpyxl
import time
import quandl
import platform # this is to tell what os we are currently using

from functions import *
from stock import *
from data import *
from sheet import *

########################################################################################


# change save path based on os
try:
    save_path = None
    if(platform.system() == "Darwin"):
        save_path = "/users/twig/Desktop/"
    else:
        save_path = "C:/Users/ericl/Desktop/"

    # get the workbook and stock list
    # depends on the file format of the template
    template_file = "test_template.txt"
    wb = None
    stock_list = []
    extension = template_file[template_file.rfind(".")+1:]
    if(extension == "xlsx"):
        wb = openpyxl.load_workbook(template_file)
        stock_list = wb.sheetnames
    elif(extension == "txt"):
        f = open(template_file, "r")
        wb = openpyxl.Workbook()
        for line in f:
            if(line[-1] == "\n"):
                stock_list.append(line[:-1])
            else:
                stock_list.append(line)
            wb.create_sheet(line, 0)
        f.close()

    print(stock_list)

    data = Data(stock_list)
    data.retrieve_data()
    short_term_data = data.get_last_3_months()

    for sheet in wb:
        stock_sheet = Stock(sheet, short_term_data[sheet.title])
        stock_sheet.format()
        stock_sheet.fill_data()
        stock_sheet.fill_stats()
        stock_sheet.fill_graphs()

    
    for month in range(1,13):
        data.get_average_percent_change("AAPL", month)

# this doesn't work to stop no wifi errors for some reason
# TODO: catch no wifi error
except ConnectionError:
    print("ERROR: NO INTERNET")

# the way the long term sheets will work is there will only be one sheet class and all it will do is put the given data into the sheet.
# thus, the Data class needs to be able to return data formatted in a specific way for every single type of data (percent change, frequency, std dev)
# as a result, every sheet will have the same functions of format, put data into the sheet, and color.
# the constructor will take in a pre-formatted data list and the color function will take in high and low values for coloring.

print("it works!")

save(wb, save_path)

# try:
#
#   fileName = "template.xlsx"
#   bins = 20
#   savePath = "C:/Users/ericl/Desktop/"
#
#   wb = openpyxl.load_workbook(fileName)
#
#   run = f.fileOpen(wb, fileName, savePath)
#
#   if(run):
#
#       # recent data
#       for sheet in wb:
#
#           print(sheet.title + " ANALYSIS")
#
#           stock = s.Stock(sheet.title, sheet, bins, savePath)
#           stock.formatRecentDataSheet()
#           hd = stock.getHistoricalData()
#           prices = stock.fillRecentData(hd)
#           stock.fillRecentDescriptiveStats(prices)
#           stock.fillRecentGraphs(prices)
#
#           print("COMPLETED\n")
#
#       # 10 year stuff
#       stockList = wb.sheetnames
#       frequencyList = []
#       stdevList = []
#
#
#       # percentage sheet
#       foo = wb.create_sheet("10YR %", 0)
#
#       percentageSheet = classes.PercentageSheet(foo, [], stockList)
#       percentageSheet.format()
#       monthMeans = percentageSheet.fill(frequencyList, stdevList)
#       percentageSheet.color()
#
#
#       # standard deviation sheet
#       foo = wb.create_sheet("10YR % STD Dev", 1)
#
#       #TODO: use monthMeans to switch std dev coloring to being percentage based
#       stdevSheet = classes.StdevSheet(foo, stdevList, stockList)
#       stdevSheet.format()
#       stdevSheet.fill()
#       stdevSheet.color()
#
#
#       # frequency sheet
#       foo = wb.create_sheet("10YR FREQ", 2)
#
#       frequencySheet = classes.FrequencySheet(foo, frequencyList, stockList)
#       frequencySheet.format()
#       frequencySheet.fill()
#       frequencySheet.color()
#
#       #save workbook
#       if (f.save(wb, savePath)):
#           print("WORKBOOK COMPLETED")
#
#       timeElapsed = time.time() - start
#       # im not sure if time will automatically cast to an int and im too lazy to look it up :D
#       print("\nELAPSED TIME:", str(int(int(timeElapsed)/60)) + "m", str(int(timeElapsed)%60)+"s")
#
# except quandl.errors.quandl_error.QuandlError:
#   if (f.save(wb, savePath)):
#       print("INCOMPLETE WORKBOOK SAVED")
#   print("===PROGRAM TERMINATED===\n")
#   timeElapsed = time.time() - start
#   # im not sure if time will automatically cast to an int and im too lazy to look it up :D
#   print("\nELAPSED TIME:", str(int(int(timeElapsed)/60)) + "m", str(int(timeElapsed)%60)+"s")
#   print("504: GATEWAY TIMEOUT ERROR")
#   print("TRY TO RUN THE PROGRAM AGAIN")
#
# except KeyboardInterrupt:
#   if (f.save(wb, savePath)):
#       print("\n\nINCOMPLETE WORKBOOK SAVED")
#   print("===PROGRAM TERMINATED===")
#   print("KEYBOARD INTERRUPT\n")
#   timeElapsed = time.time() - start
#   # im not sure if time will automatically cast to an int and im too lazy to look it up :D
#   print("\nELAPSED TIME:", str(int(int(timeElapsed)/60)) + "m", str(int(timeElapsed)%60)+"s")
#
# except ConnectionResetError:
#   if (f.save(wb, savePath)):
#       print("\n\nINCOMPLETE WORKBOOK SAVED")
#   print("===PROGRAM TERMINATED===\n")
#   print("CONNECTION RESET ERROR\n")
#   timeElapsed = time.time() - start
#   # im not sure if time will automatically cast to an int and im too lazy to look it up :D
#   print("\nELAPSED TIME:", str(int(int(timeElapsed)/60)) + "m", str(int(timeElapsed)%60)+"s")
