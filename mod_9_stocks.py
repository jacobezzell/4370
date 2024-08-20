"""
Jacob Ezzell
August 12th 2024
ICS 4370
Description: display using pandas
"""
import matplotlib.pyplot as plt
import pandas as pd
import os

#define the path from this file to the stored data
file_path="c:/DU Python/4370/stockdata/"

#use list comprehension and a filter to only pull the .csv files from the directory
#drop the last 4 characters of each list to get just the filename without the extension
files = [f[:-4] for f in os.listdir(file_path) if f.endswith('.csv')]


#create an empty dictionary to hold all the dataframes from the CSV file
df_list={}

for file in files:
    #read the data from the appropriate csv
    try:
        df_list[file]=pd.read_csv(f"{file_path}{file}.csv")
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

#print(df_pivot)

#Find the total value of the portfolio each day by adding the values across. But drop out the SPY since
df_pivot_nospy = df_pivot.drop("SPY")
df_pivot_nospy["Total"] = df_pivot_nospy.sum(axis=1)


#make the correlation calculation, note this makes a series, not a dataframe.
correlation_with_SPY = df_pivot.corrwith(df_pivot['SPY'])

#label the column, so make this a dataframe first.
df_corr = correlation_with_SPY.to_frame() 
df_corr.columns = ['Correlation Coefficient']
print(df_corr)

#print the various stocks with a line drawing
# Plot all columns. dataframes to matplot is just too easy.
df_pivot.plot(kind="line", figsize=(12, 6))

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Stock Prices Over Time')
plt.legend()
plt.grid(True)
plt.show()