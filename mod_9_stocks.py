"""
Jacob Ezzell
August 12th 2024
ICS 4370
Description: display using pandas
"""
import matplotlib.pyplot as plt
import pandas as pd

#create a list of all the files to import
files = ["AIG", "F", "FB", "GOOG", "IBM", "M", "MSFT", "RDS-A", "SPY"]

#create an empty dictionary to hold all the dataframes from the CSV file
df_list={}

for file in files:
    #read the data from the appropriate csv
    try:
        df_list[file]=pd.read_csv('stockdata/'+file+'.csv')
        #insert a column to hold the ticker indicator for this file
        df_list[file].insert(0,'Ticker',file)
        #display a sampling
        #print(df_list[file].head())
    except:
        print('Unable to read stockdata/'+file+'.csv')


#mush them all together into one big happy dataframe
df_all = pd.concat(df_list.values(), ignore_index=True)

#print(df_all)

summary = df_all.groupby('Ticker')['Close'].agg(['mean', 'std'])
print(summary)

#create a dataframe with the closing price for each stock
df_pivot = df_all.pivot(index='Date', columns='Ticker', values='Close')

print(df_pivot)
#make the correlation calculation, note this makes a series, not a dataframe.
correlation_with_SPY = df_pivot.corrwith(df_pivot['SPY'])

#label the column, so make this a dataframe first.
df_corr = correlation_with_SPY.to_frame() 
df_corr.columns = ['Correlation Coefficient']
print(df_corr)

#print the various stocks with a line drawing
# Plot all columns. dataframes to matplot is just too easy.
df_pivot.plot(figsize=(12, 6))

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Stock Prices Over Time')
plt.legend()
plt.grid(True)
plt.show()