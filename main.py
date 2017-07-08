from openpyxl import *
import numpy as np

import functions as f

fileName = "template.xlsx"
# fileName = "test_template.xlsx"

wb = load_workbook(fileName)

run = f.fileOpen(wb, fileName)

print("\n")
print("===STARTING RECENT DATA ANALYSIS")
print("\n")

if(run):

	#iterate through the sheets
	for sheet in wb:

		f.clean(sheet)

		print ("SHEET TITLE:       " + sheet.title)	

		prices = f.fillData(sheet)

		f.fillStats(sheet, prices)

		f.graphs(sheet, prices)

		#finish
		print(sheet.title + " RECENT DATA ANALYSIS COMPLETE\n")

	print("\n===ALL RECENT DATA ANALYSIS COMPLETE===\n\n")

	print("===STARTING 10 YEAR DATA ANALYSIS===\n\n")

	f.tenYearAverage(wb)

	#save workbook
	if (f.save(wb)):
		print("WORKBOOK COMPLETED")