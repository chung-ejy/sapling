from extractor.fred_extractor import FREDExtractor
from database.adatabase import ADatabase
import numpy as np
fred = FREDExtractor
fed = ADatabase("fed")

fed.connect()
fed.drop("cpi")
fed.drop("exports")
fed.drop("gdp")
fed.drop("unrate")
fed.drop("treasury_yields")
fed.drop("oil")
fed.drop("sp500")
#fed.store("cpi",fred.cpi().replace(".",np.nan).dropna())
fed.store("exports",fred.exports().replace(".",np.nan).dropna())
fed.store("gdp",fred.gdp().replace(".",np.nan).dropna())
fed.store("unrate",fred.unrate().replace(".",np.nan).dropna())
fed.store("treasury_yields",fred.treasury_yields().replace(".",np.nan).dropna())
fed.store("oil",fred.oil().replace(".",np.nan).dropna())
fed.store("sp500",fred.sp500().replace(".",np.nan).dropna())
fed.disconnect()
