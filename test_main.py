from data_processing import Data

data = Data(["AAPL", "PYPL", "SPGI", "PSX", "ZTS"])
# Data(["AAPL"])
# 

data.get_data()

data.compute_summary_statistics()

data.cut_long_term_data()

data.get_monthly_percent_change()

data.compute_monthly_change()

data.compute_monthly_frequency()


# various prints to make sure our data is collected properly
print("monthly percent change average")
print(data.monthly_change_data)
print()

print("monthly percent change frequency")
print(data.monthly_frequency_data)
print()

print("short term data")
print(data.stocks_short_term_data)
print()

print("summary statistics")
print(data.summary_statistics)
print() 