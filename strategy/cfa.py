from strategy.astrategy import AStrategy

class CFA(AStrategy):

    def __init__(self,cycle):
        super().__init__("cfa",cycle)
        self.projection_horizon = (365 / 7) * 5
    