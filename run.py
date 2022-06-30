# Eric Liu

# The main function. This parses command line arguments or optionally takes the single input of
# a dictionary that simulates running from the command line

from tqdm import tqdm

import argparse
import time
import quandl
import json
import os
import datetime

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

    :return:    str         The name of the saved wb
    """
    # if this project is being called from the website
    if(params is not None):
        args = params
    else:
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
        parser.add_argument("-l", "--log", action="store_true",
            help="Include this flag to log errors")
        parser.add_argument("--quandl", type=str, nargs=1, help="Your Quandl API key. " \
            "This key should have access to the EOD and QOR premium databases (~$1250 per year). " \
            "This flag sets the value to the env key \"QUANDL_API_KEY\". If your enviorment already " \
            "has the key set, you do not need to use this flag.")
        args = vars(parser.parse_args())

    # if the user inputed a quandl api key, add it to the env variables
    if(args["quandl"] is not None):
        os.environ["QUANDL_API_KEY"] = args["quandl"][0]

    # if using the --test flag, use the default config file and overwrite data
    if(args["test"]):
        args["config"] = "config/default.json"
        args["overwrite"] = True

    # get the requested config file
    config = get_params(args["config"])
    config["log"] = args["log"]

    # if parameters were provided from the web app, overwrite the tickers modify the paths
    if(params is not None):
        # overwrite tickers
        config["tickers"] = params["tickers"]
        
        # modify paths

        config["data_path"] = os.path.join(params["sd_root"], config["data_path"])
        config["save_location"] = os.path.join(params["sd_root"], config["save_location"])

    # if using the --test flag, change the tickers
    if(args["test"]):
        config["tickers"] = ["AAPL", "ZTS", "ABCD", "AAPL"]

    # ensure that duplicate tickers are removed
    from collections import OrderedDict
    config["tickers"] = list(OrderedDict.fromkeys(config["tickers"]))

    # set the error logging file to an environment variable
    # the file will look something like: "2021-07-14_10:44:14:642246.log"
    os.environ["ERROR_LOG_FILE"] = os.path.join(make_absolute(config["error_logs"]), 
        str(datetime.datetime.now()).replace(" ", "_").replace(".", ":").replace(":", "-") + ".log")
        
    # download/overwrite data if requested
    if(args["overwrite"]):
        run_data(config)

    # put the processed data into an xl sheet
    return run_sheet(config)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Runtime ---{time.time() - start_time:.2f} seconds---")

