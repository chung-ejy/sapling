
class IndustryDiversifier(object):
    
    def __init__(self):
        self.name = "industry_diversifier"

    def diversify(self,todays_sim,index):
        sectors = todays_sim["gics sector"].unique()
        sectors.sort()
        return todays_sim[todays_sim["gics sector"]==sectors[index]]