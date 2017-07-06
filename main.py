from openpyxl import *
import numpy as np

import functions as f

fileName = "template.xlsx"

wb = load_workbook(fileName)

run = f.fileOpen(wb, fileName)


if(run):
	#iterate through the sheets
	for sheet in wb:
		# try:
		f.clean(sheet)

		#gets the stock from the sheet name
		print ("SHEET TITLE:       " + sheet.title)	

		prices = f.fillData(sheet)

		f.fillStats(sheet, prices)

		f.graphs(sheet, prices)

		# except AttributeError:
		# 	print("AttributeError")
		# 	sheet.column_dimensions["A"].width = 24
		# 	sheet["A1"] = "ERROR: STOCK DOES NOT EXIST"
		# except KeyError:
		# 	print("KeyError")
		# 	sheet.column_dimensions["A"].width = 24
		# 	sheet["A1"] = "ERROR: STOCK DOES NOT EXIST"
		# except TypeError:
		# 	print("TypeError")
		# 	sheet.column_dimensions["A"].width = 24
		# 	sheet["A1"] = "ERROR: STOCK DOES NOT EXIST"

		#finish
		print(sheet.title + " COMPLETED\n")

	#save workbook
	if (f.save(wb)):
		print("WORKBOOK COMPLETED")