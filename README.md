# Stock-Data

When run, generates an excel doc that gives various stats for short term and long term time periods. The stocks that are analyzed must exist in the free Quandl WIKI/PRICES database (support for Alpha Vantage is in the works and a yahoo finaince data scraper is planned) and are choosen based on the sheet titles in the file template.xlsx or template.txt.

If the template file is an excel workbook, there must be one sheet for every stock. The title of each sheet must be the name of the stock and the sheet itself must be blank. If the template file is a text document, stocks must be listed with one on each line with no newlines at the front and one newline at the end. If these rules are not followed then there is a chance that the program will not work properly.

The short term time period is 60 days, about 3 months (20 trading days per month). Descriptive statistics (n, mean, 60, 40, and 20 day standard deviations), a 20 bin histogram, and a line chart are generated and put in a sheet titled with the stock name.

The long term time period is 10 years. The program will calculate the average historical percentage change, the standard deviation of the percentage change, and the frequency of which the price goes up or down over the course of a month for the stock. All information for all stocks is compiled into three new sheets that will appear in front of the stocks in template.xlsx.

:D
