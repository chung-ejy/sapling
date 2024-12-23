from strategy.coev_weekly import COEVWeekly
from strategy.rolling_average_quarterly import RollingAverageQuarterly
from strategy.rolling_average_weekly import RollingAverageWeekly
from strategy.magnificent_seven_quarterly import MagnificentSevenQuarterly
import pandas as pd
import matplotlib.pyplot as plt

strategy = MagnificentSevenQuarterly()
strategy.db.connect()
states = strategy.db.retrieve("states")
strategy.db.disconnect()
asset_dfs = []
for row in states.iterrows():
    assets = pd.DataFrame(row[1]["assets"])
    assets["cash"] = row[1]["cash"]
    asset_dfs.append(assets)

analysis_df = pd.concat(asset_dfs)
portfolio_df = analysis_df.groupby("date").agg({"cash":"mean","book_value":sum}).reset_index()
portfolio_df["portfolio_value"] = portfolio_df["book_value"] + portfolio_df["cash"]
plt.plot(portfolio_df["date"],portfolio_df["portfolio_value"])
plt.show()

trades = analysis_df.sort_values("date").groupby(["purchase_date","ticker"]).nth(-1).reset_index()
trades["pnl"] = (trades["adjclose"] - trades["purchase_price"]) / trades["purchase_price"]
trades["pnl"] = [row[1]["pnl"] if row[1]["exposure"]=="long" else row[1]["pnl"]*-1 for row in trades.iterrows()]
trades["color"] = ["blue" if x == "long" else "red" for x in trades["exposure"]]
# plt.scatter(trades["date"],trades["pnl"],s=10,c=trades["color"])
# plt.show()
trades["year"] = trades["date"].dt.year
trades["quarter"] = trades["date"].dt.quarter
# Compute average PnL for each date and exposure type
average_pnl_df = trades.groupby(["year", "quarter", "exposure"]).agg({"pnl": "mean"}).reset_index()

# Pivot the data to align long and short exposures by year and quarter
pivoted_pnl = average_pnl_df.pivot(index=["year", "quarter"], columns="exposure", values="pnl").fillna(0)

# Create a combined label for year and quarter for x-axis
pivoted_pnl["label"] = [f"{year}-Q{quarter}" for year, quarter in pivoted_pnl.index]
labels = pivoted_pnl["label"]

# Extract long and short PnL data
long_pnl = pivoted_pnl.get("long", pd.Series(0, index=labels))  # Default to 0 if "long" is missing
short_pnl = pivoted_pnl.get("short", pd.Series(0, index=labels))  # Default to 0 if "short" is missing

# Plot the bar chart
fig, ax = plt.subplots(figsize=(12, 6))

bar_width = 0.4  # Adjust for spacing
x_positions = range(len(labels))  # Positions for the bars
ax.bar([x - bar_width / 2 for x in x_positions], long_pnl, width=bar_width, color="blue", label="Long")
ax.bar([x + bar_width / 2 for x in x_positions], short_pnl, width=bar_width, color="red", label="Short")

# Add labels, legend, and title
ax.set_xlabel("Year-Quarter")
ax.set_ylabel("Average PnL")
ax.set_title("Average PnL by Exposure Type Over Time")
ax.set_xticks(x_positions)
ax.set_xticklabels(labels, rotation=45)
ax.legend()

plt.tight_layout()
plt.show()
