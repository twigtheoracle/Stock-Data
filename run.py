# Eric Liu

# The main function. This parses command line arguments or optionally takes the single input of
# a dictionary that simulates running from the command line

from tqdm import tqdm

import argparse
import time
import quandl
import json
import os

from src.functions import *
from src.data.run_data import run_data
from src.sheet.run_sheet import run_sheet

########################################################################################

def main(params=None):
    """
    The main function which calls all other functions

    :param:     params      Optional params which simulate running from the command line, used to 
                            run the project from the website. It is expected for params to be a 
                            dictionary with key/value for every command line arg below
    """
    # read and process command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, nargs=1, metavar="str", 
        default="config/default.json", help="The path to the desired config file. By default " \
        "this takes the value of \"config/default.json\"")
    parser.add_argument("--test", action="store_true",
        help="When present, the program will override the \"tickers\" parameter of the config " \
        "file to only process on AAPL and ZTS.")
    parser.add_argument("-o", "--overwrite", action="store_true",
        help="Download/overwrite existing data. This flag must be passed in everytime the " \
        "tickers change or the data save location changes")
    parser.add_argument("--quandl", type=str, nargs=1, help="Your Quandl API key. " \
        "This key should have access to the EOD and QOR premium databases (~$1250 per year). " \
        "This flag sets the value to the env key \"QUANDL_API_KEY\". If your enviorment already " \
        "has the key set, you do not need to use this flag.")
    args = vars(parser.parse_args())

    # if this project is being called from the website
    if(params is not None):
        args = params

    # if the user inputed a quandl api key, add it to the env variables
    if(args["quandl"] is not None):
        os.environ["QUANDL_API_KEY"] = args["quandl"][0]

    # if using the --test flag, use the default config file and overwrite data
    if(args["test"]):
        args["config"] = "config/default.json"
        args["overwrite"] = True

    # get the requested config file
    config = get_params(args["config"])

    # if using the --test flag, change the tickers
    if(args["test"]):
        config["tickers"] = ["AAPL", "ZTS"]

    # download/overwrite data if requested
    if(args["overwrite"]):
        run_data(config)

    # put the processed data into an xl sheet
    run_sheet(config)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Runtime ---{time.time() - start_time:.2f} seconds---")

