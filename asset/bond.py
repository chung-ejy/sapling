class Bond(object):

    def __init__(self,ticker="",adjclose=0,quantity=0):
        self.ticker = ticker
        self.adjclose = adjclose
        self.quantity = quantity
        self.coupon_rate = 0.05
    
    def update(self, row):
        self.rate = row["rf"]

    def buy(self, row, notional):
        self.ticker = row["ticker"]
        self.buy_date = row["date"]
        self.sell_date = None
        
        
        # Calculate bond price considering coupon payments
        self.adjclose = self.calculate_price(
            face_value=1000,
            rate=row["rf"],
            coupon_rate=self.coupon_rate,
            years=10
        )
        
        self.quantity = notional / self.adjclose
        self.rate = row["rf"]
        self.pv = self.adjclose * self.quantity
    
    def calculate_price(self,face_value, rate, coupon_rate, years):
        """
        Calculate bond price considering coupon payments.
        face_value: The face value of the bond (e.g., $1000)
        rate: The market interest rate (discount rate)
        coupon_rate: The annual coupon rate of the bond
        years: The number of years to maturity
        """
        # Coupon payment is face value times coupon rate
        coupon_payment = face_value * coupon_rate
        price = 0
        
        # Present value of all coupon payments
        for t in range(1, years + 1):
            price += coupon_payment / (1 + rate) ** t
        
        # Present value of the face value
        price += face_value / (1 + rate) ** years
        
        return price
