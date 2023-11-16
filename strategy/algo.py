from strategy.astrategy import AStrategy

class Algo(AStrategy):

    def __init__(self,cycle):
        super().__init__("algo",cycle)
        self.projection_horizon = 5
    