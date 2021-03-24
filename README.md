
# Stock-Data

This project automates the generation of Excel spreadsheets containing various stock price/IV data. The data for this project comes from Quandl, from the paid datasets of [QOD](https://www.quandl.com/data/QOR-US-Equity-Option-Ratings) (US Equity Option Ratings) and [EOD](https://www.quandl.com/data/EOD-End-of-Day-US-Stock-Prices) (End of Day US Stock Prices).

Three long term (10 years) sheets are generated showing monthly percent change, monthly percent change standard deviation, and monthly positive gain frequency. One short term sheet is generated for every stock in the ticker list, with each short term sheet showing three month (60 trading days) price history, IV30 percentile, IV30 rank, and IV30 Rating. For a description of what IV30___ means, see the [documentation page](https://www.quandl.com/data/QOR-US-Equity-Option-Ratings/documentation) for the QOR dataset.

See the file sample.xlsx for a better idea of what the project generates.

## How to Run
You can run the project through my website (WIP) and through the command line interface.

### Website
WIP

### Command Line Interface

 1. Clone the project anywhere
 2. Navigate to the project directory and run the command "pip install -r requirements.txt". Note the project requires Python 3.X
 3. Test that the project successfully installed by running the command "python run.py --test --quandl {QUANDL_API_KEY}". Make sure to input your Quandl API key in the {}
 4. For a description of all possible command line arguments, see below

## Description of Parameters
### Command Line Arguments
|Flag|Type|Default Value|Description|
|-|-|-|-|
|-c, -\-config|str|"config/default.json"|Where to find the settings file|
|-\-test|bool|False|Test the program on the tickers of "AAPL" and "ZTS". Using this flag will always overwrite data and use the default config file.|
|-\-overwrite|bool|False|Whether or not to overwrite data. This flag should be included everytime the stock list changes, running the program on different days, or with a fresh clone of the project.|
|-\-quandl|str|None|Your Quandl API key. The key can be found on you [Quandl Profile Page](https://www.quandl.com/account/profile). The account associated with the key must have subscriptions to the QOD and EOD premium datasets. This key is not necessary if you are not downloading data (-\-overwrite is not present), or if your Quandl API key is stored in your local environment under the key "QUANDL_API_KEY". This means that the python code "os.environ["QUANDL_API_KEY"]" will return your key.|

### Configuration Arguments
These are by default found in the file "config/default.json"
|Key|Type|Default Value|Description|
|-|-|-|-|
|data_path|str|"data/"|The folder where data is saved to.|
|raw_folder|str|"raw/"|The folder where raw data is saved to.|
|adj_close_folder|str|"adj_close/"|The folder where EOD data is saved to. The full path by default is "data/raw/adj_close/"|
|iv_folder|str|"iv/"|The folder where QOD data is saved to. The full path by default is "data/raw/iv/"|
|processed_folder|str|"processed/"|The folder where cleaned data is saved. The full path by default is "data/processed/"|
|save_location|str|"xl_sheets/"|The folder where generated Excel sheets are saved|
|tickers|[strs]|*|The list of tickers to generate the Excel sheets for|
|num_bins|int|15|The number of bins to use when creating short term data histograms|
|color_gradient|[strs]|*|The list of colors (hex color codes) that define the color gradient to use. By default, the gradient is formed with 20 colors from red (#E4001A) to green (#0CDE17)|
|perc_low_high|[int, int]|[-5, 10]|The values that correspond go the lowest (red) percent change to the highest (green) percent change|
|std_low_high|[int, int]|[10, 3]|The values that correspond go the lowest (red) standard deviation to the highest (green) standard deviation|
|freq_low_high|[int, int]|[0, 100]|The values that correspond go the lowest (red) frequency to the highest (green) frequency|

\* These default values are too long to include here, look in the actual file "config/default.json"

Last Updated: March 23rd, 2021
