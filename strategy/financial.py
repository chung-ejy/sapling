from strategy.astrategy import AStrategy

class Financial(AStrategy):

    def __init__(self,cycle):
        super().__init__("financial",cycle)
        self.projection_horizon = 60
    