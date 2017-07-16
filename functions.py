from string import ascii_uppercase
from datetime import *
from scipy import stats
from openpyxl.chart import BarChart, Series, Reference, LineChart

import pprint
import math
import pprint
import sys

################################################################################

# checks if the file is open
# return	True	file is closed (can save)
# return	False	fils is open (can not save)
def fileOpen(wb, fileName, path):
	try:
		wb.save(fileName)
		return True
	except PermissionError:
		print("ERROR: FILE IS OPEN")
		print("CLOSE FILE AND RUN SCRIPT AGAIN")
		return False

################################################################################

# saves the completed workbook as option_analysis_ and the current date
# return 	True 	if the save completed successfully
# return 	False 	if the save didn't go through
def save(wb, path):
	try:
		wb.save(path + "option_analysis_" + str(date.today()) + ".xlsx")
		return True
	except PermissionError:
		print("ERROR: FILE IS OPEN")
		print("CLOSE FILE AND RUN SCRIPT AGAIN")
		return False

################################################################################

# tests is the input is a number
# return 	True	n is a number
# return 	False 	n is not a number
def isNumber(n):
	try:
		int(n)
		return True
	except ValueError:
		return False

################################################################################

# returns a list of the next three months based on the current month
# return 	returnList	a list of the next three month numbers
def getMonthList(currentMonth):
	returnList = [0] * 3
	for i in range(1,3):
		returnList[i] = (currentMonth + i) % 12
	for i in range(0,3):
		if (returnList[i] == 0):
			returnList[i] = 12
	return returnList
