import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime

# Sample data
dates = [datetime.datetime(2023, i, 1) for i in range(1, 13)]
values = np.random.randn(12)

# Create the plot
fig, ax = plt.subplots()
ax.plot(dates, values)

# Format dates
date_format = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

plt.show()