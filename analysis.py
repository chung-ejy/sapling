import pandas as pd
import matplotlib.pyplot as plt
from database.adatabase import ADatabase
db = ADatabase("algo")
db.connect()
report = db.retrieve("reports")
db.disconnect()

print(report.sort_values("cr").tail(50))
plt.scatter(report["avg_risk"].values,report["cr"].values,c=report["rr"].values,cmap="RdYlGn",s=report["risk"].values)
plt.show()


query = report.sort_values("cr").tail(1)[["rolling_val","projection_week"]].to_dict("records")[0]
db.connect()
trades = db.query("trades",query)
db.disconnect()
print(trades)
plt.plot(trades["date"].values,trades["cr"].values)
plt.show()