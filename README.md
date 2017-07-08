# Stock-Data

When run, generates an excel doc that gives various stats for short term and long term time periods. The stocks that are analyzed must exist in the free Quandl WIKI/PRICES database and are choosen based on the sheet titles in the file template.xlsx.

The short term time period is 60 days, about 2 months. Descriptive statistics (n, mean, 60, 40, and 20 day standard deviations), a 20 bin histogram, and a line chart are generated and put in a sheet titled after the stock.

The long term time period is 10 years. The program will calculate the average historical percentage change, the standard deviation of the percentage change, and the frequency of which the price goes up or down over the course of a month for the stock. All information for all stocks is compiled into three new sheets that will appear in front of the stocks in template.xlsx.

Also why are you viewing this repository?
