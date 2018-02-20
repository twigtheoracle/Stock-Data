# Stock-Data

When run, generates an excel doc that gives various stats for short term and long term time periods. The stocks that are analyzed must exist in the free Quandl WIKI/PRICES database (support for Alpha Vantage is in the works and a yahoo finaince data scraper is planned) and are choosen based on the sheet titles in the file template.xlsx or template.txt.

If the template file is an excel workbook, there must be one sheet for every stock. The title of each sheet must be the name of the stock and the sheet itself must be blank. If the template file is a text document, stocks must be listed with one on each line with no newlines at the front and one newline at the end. If these rules are not followed then there is a chance that the program will not work properly.

The short term time period is 60 days, about 3 months (20 trading days per month). Descriptive statistics (n, mean, 60, 40, and 20 day standard deviations), a 20 bin histogram, and a line chart are generated and put in a sheet titled with the stock name.

In order to run this program, you need to have (at the time of last update), one of two different API keys. Before getting the keys though, first you need to make a file called "api_key.py" in the same folder as main. If you want to use Quandl (suggested for speed), you must get a Quandl key (free) and create a function in api_key.py called get_Quandl_API_key(). This function should only return the key as a string. If you want to use Alpha Vantage (optimization in progress), you must get a AV key from their website (also free) and create a function called get_AV_API_key(): which will only return the key as a string. Finally, in main.py change line 29 (this may change but you can just search for data_provider) to be the correct data provider, either "Quandl" or "AV".

In addition, before you run this program, you need a template file of some sort. This can either be a .txt file or a .xlsx file. If your template file is a text file, you must format it with no leading newlines, and one trailing newline, with every desired stock on a different line. If your template file is an excel sheet, your workbook must have one sheet for every stock, where the sheet title is the stock. Finally every sheet should be completly blank and unformatted.

Once you have taken care of all those annoying things (I'm working on a GUI to make this easier), all you have to do is run main.py from the console and watch the magic happen (at least I hope).

Last Updated: 1/19/2018
