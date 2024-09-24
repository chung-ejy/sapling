class Bond(object):

    @classmethod
    def update(cls, row, asset):
        updated = asset.copy()
        # # Calculate bond price considering coupon payments
        # updated["adjclose"] = cls.calculate_price(
        #     face_value=1000,
        #     rate=row["rf"],
        #     coupon_rate=asset.get("coupon_rate", 0.05),  # Default 5% coupon rate
        #     years=10
        # )
        # updated["pv"] = updated["adjclose"] * updated["quantity"]
        return updated

    @classmethod
    def sell(cls, row, asset):
        updated = asset.copy()
        updated["sell_date"] = row["date"]
        return updated

    @classmethod
    def buy(cls, row, asset, notional, asset_type="bond", coupon_rate=0.05):
        updated = asset.copy()
        updated["ticker"] = row["ticker"]
        updated["buy_date"] = row["date"]
        updated["sell_date"] = None
        updated["asset_type"] = asset_type
        updated["coupon_rate"] = coupon_rate
        
        # Calculate bond price considering coupon payments
        updated["adjclose"] = cls.calculate_price(
            face_value=1000,
            rate=row["rf"],
            coupon_rate=coupon_rate,
            years=10
        )
        
        updated["quantity"] = notional / updated["adjclose"]
        updated["rate"] = row["rf"]
        updated["pv"] = updated["adjclose"] * updated["quantity"]
        return updated
    
    @staticmethod
    def calculate_price(face_value, rate, coupon_rate, years):
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
