
class BaseDiversifier(object):
    
    def __init__(self):
        self.name = "industry_diversifier"

    def diversify(self,todays_sim,index,number_of_positions):
        todays_sim["weight"] = float(1/number_of_positions)
        return todays_sim