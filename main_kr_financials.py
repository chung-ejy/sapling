import pandas as pd
from strategy.kr_financial_statement_yearly import KRFinancialStatementYearly

strat = KRFinancialStatementYearly()
strat.load_dataset()