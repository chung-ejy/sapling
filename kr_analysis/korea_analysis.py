#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


portfolio = pd.read_csv("portfolio.csv")
trades = pd.read_csv("trades.csv")
kospi = pd.read_excel("kospi.xlsx").rename(columns={"Ticker":"ticker"})[1:][["Name","ticker"]]
kospi["ticker"] = [int(x) for x in kospi["ticker"]]
trades = trades.merge(kospi,on="ticker",how="left")
trades["count"] = 1


# In[3]:


kospi


# In[4]:


portfolio["rolling_return"] = portfolio["return"].rolling(10).mean()


# In[5]:


fig, ax = plt.subplots()
ax.plot(portfolio["rolling_return"].values)
fig.set_size_inches(12, 4) 
plt.show()


# In[6]:


ticker_view = trades.groupby(["ticker","Name"]).aggregate({"return":"mean","count":"sum"}).sort_values("count",ascending=False).reset_index().head(10)
ticker_view["return"] = ticker_view["return"] + 1
ticker_view["total_return"] = ticker_view["return"] ** ticker_view["count"]
ticker_view.sort_values("count",ascending=False).head(20)


# In[7]:


plt.scatter(trades["coefficient_of_variance"],trades["return"],s=1)
plt.show()


# In[8]:


import matplotlib.pyplot as plt
import mplcursors
from matplotlib.ticker import MaxNLocator

# Assuming portfolio is a Pandas DataFrame with a "date" column and a "cumulative_return" column

fig, ax = plt.subplots()
line, = ax.plot(portfolio["date"], portfolio["cumulative_return"].values)

# Set the figure size
fig.set_size_inches(12, 4)

# Use MaxNLocator to automatically choose a suitable number of ticks on the x-axis
ax.xaxis.set_major_locator(MaxNLocator(nbins=10))  # You can adjust the number of ticks as needed

# Rotate the x-axis labels for better visibility if necessary
plt.xticks(rotation=45)

# Add hover labels using mplcursors
cursor = mplcursors.cursor(hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(
    f'Point of Interest: {sel.target[1]:.2f}'))

plt.show()


# In[ ]:




