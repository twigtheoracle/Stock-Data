from pprint import pprint
from tqdm import tqdm

import openpyxl
import time
import quandl

from functions import *
from stock import *
from data import *
from sheet import *
from errors import *

########################################################################################

def main():

    start = time.time()

    try:
        save_path = get_save_path()

        # get the workbook and stock list
        # depends on the file format of the template
        template_file = "template.txt"
        wb, stock_list = get_workbook_and_stocklist(template_file)

        data = Data(stock_list)
        data.retrieve_data(data_provider = "Quandl")
        short_term_data = data.get_short_term_data()

        print("\ncreating stock sheets...")
        for sheet in wb:
            stock_sheet = Stock(sheet, short_term_data[sheet.title])
            stock_sheet.format()
            stock_sheet.fill_data()
            stock_sheet.fill_stats()
            stock_sheet.fill_graphs()
        print("done")
        
        long_term_data = data.get_long_term_data()

        temp_sheet = wb.create_sheet("10YR %", 0)
        percentage_sheet = Sheet(temp_sheet, long_term_data["percent_change"], stock_list, long_term_data["years"])
        percentage_sheet.format()
        percentage_sheet.fill()
        percentage_sheet.color(-10, 10)

        temp_sheet = wb.create_sheet("10YR % STD DEV", 1)
        # note: std dev here is std dev of percentage change, not of average value of the month
        std_dev_sheet = Sheet(temp_sheet, long_term_data["std_dev"], stock_list, long_term_data["years"])
        std_dev_sheet.format()
        std_dev_sheet.fill()
        # TODO: do some work to figure out optimal numbers for std dev coloring
        std_dev_sheet.color(.1, .02)

        temp_sheet = wb.create_sheet("10YR FREQ", 2)
        freq_sheet = Sheet(temp_sheet, long_term_data["freq"], stock_list, long_term_data["years"])
        freq_sheet.format()
        freq_sheet.fill()
        freq_sheet.color(20, 80)

    # this doesn't work to stop no wifi errors for some reason
    # TODO: catch no wifi error
    except ConnectionError:
        print("\nERROR: NO INTERNET")
    except requests.exceptions.SSLError:
        print("\nERROR: SSL Certificate is not valid")
    except quandl.errors.quandl_error.QuandlError:
        print("\nERROR: Quandl Speed Limit Breached")
        
    time_elapsed = time.time() - start
    print()
    print("time elapsed: " + str(int(int(time_elapsed) / 60)) + "m " + str(int(time_elapsed) % 60) + "s")

    save(wb, save_path)

if __name__ == '__main__':
    main()

