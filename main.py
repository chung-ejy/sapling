from parameter.aparameter import AParameter
from strategy.astrategy import AStrategy

ap = AParameter()
ap.build({"cycle":100})
print(ap.__dict__)
astrat = AStrategy("algo",ap)
print(astrat)