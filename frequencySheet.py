from openpyxl.styles import Color, PatternFill

import openpyxl
import datetime
import string

import sheet

class frequencySheet(sheet.Sheet):
	# colors the frequecy sheet on a red green gradient
	def color(self):
		for letter in range(2, 15): # from letter B to N when plugged into the first non __init__ function
			for row in range(3, 3 + len(self.stockList)):
				cell = self.numberToLetter(letter) + str(row)
				value = self.sheet[cell].value

				if (value != None):
					value = int(value/5)
					if (value <= 0):
						value = 0
					elif (value >= 19):
						value = 19
					self.sheet[cell].fill = self.colorGradient[value]
