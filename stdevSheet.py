from openpyxl.styles import Color, PatternFill

import openpyxl
import datetime
import string

import sheet

class stdevSheet(sheet.Sheet):
	# colors the stdev sheet on a red green gradient
	def color(self):
		for letter in range(2, 15): # from letter B to N 
			for row in range(3, 3 + len(self.stockList)):
				cell = self.numberToLetter(letter) + str(row)
				value = self.sheet[cell].value

				if (value != None and value != -1):
					value = 20-int(value*2)
					if (value <= 0):
						value = 0
					elif (value >= 19):
						value = 19
					self.sheet[cell].fill = self.colorGradient[value]