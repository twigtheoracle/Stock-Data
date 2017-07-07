from openpyxl import *
import numpy as np

import functions as f

fileName = "test_template.xlsx"

wb = load_workbook(fileName)

run = f.fileOpen(wb, fileName)


if(run):

	#iterate through the sheets
	for sheet in wb:

		f.clean(sheet)

		print ("SHEET TITLE:       " + sheet.title)	

		prices = f.fillData(sheet)

		f.fillStats(sheet, prices)

		f.graphs(sheet, prices)

		#finish
		print(sheet.title + " COMPLETED\n")

	f.tenYearAverage(wb)

	#save workbook
	if (f.save(wb)):
		print("WORKBOOK COMPLETED")