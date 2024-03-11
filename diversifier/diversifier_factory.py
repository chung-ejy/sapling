from diversifier.diversifier import Diversifier
from diversifier.industry import Industry
from diversifier.index_correlation import IndexCorrelation
from diversifier.simple import Simple
class DiversifierFactory(object):

    @classmethod
    def build(self,name):
        match name:
            case Diversifier.INDUSTRY.value:
                return Industry()
            case Diversifier.INDEX_CORRELATION.value:
                return IndexCorrelation()
            case Diversifier.SIMPLE.value:
                return Simple()
            case _:
                return None
