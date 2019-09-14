from data_processing import Data

data = Data(["AAPL", "PYPL", "SPGI", "PSX", "ZTS"])
# Data(["AAPL"])
# 

data.get_data()

data.cut_long_term_data()