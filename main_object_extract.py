from strategy.single_index_quarterly import SingleIndexQuarterly
from strategy.magnificent_seven_quarterly import MagnificentSevenQuarterly
from strategy.financial_statement_quarterly import FinancialStatementQuarterly
from strategy.korean_tech_quarterly import KoreanTechQuarterly
from strategy.optimal_quarterly import OptimalQuarterly
from strategy.kr_financial_statement_yearly import KRFinancialStatementYearly
strategies = [
                KRFinancialStatementYearly()
                ,KoreanTechQuarterly()
              ,SingleIndexQuarterly()
              ,MagnificentSevenQuarterly()
              ,FinancialStatementQuarterly()
              ]

for strategy in strategies:
    strategy.load_dataset()