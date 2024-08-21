"""
Jacob Ezzell
August 20th 2024
ICS 4370
Description: display stock data from a json file
"""
from datetime import date, datetime
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sqlite3
import json
import pandas as pd
import os


#define an investor class
class Investor:
    def __init__(self, investor_id, name, address):
        self.investor_id = investor_id
        self.name = name
        self.address = address
        #list to contain the investor's stock objects
        self.stockdata= []

    def add_stockdata(self, purchase_id, stock_ticker, stock_date, stock_open, stock_high, stock_low, stock_close, stock_adj_close, stock_volume):
        new_stock = Stock(purchase_id, stock_ticker, stock_date, stock_open, stock_high, stock_low, stock_close, stock_adj_close, stock_volume)
        self.stockdata.append(new_stock)

    def pandafy_stocks(self):
        for stock in self.stockdata:
            #return the stockdata into a pandas dataframe.
            df = pd.DataFrame(columns=["ticker", "date", "close"])
            print(df)

            for stock in self.stockdata:
                new_row = {"ticker":stock.ticker, "date":stock.date, "close":stock.close}
                #print(new_row)
                df.loc[len(df)] = new_row

            return df
           
#define the stock class:
class Stock:  #Date,Open,High,Low,Close,Adj Close,Volume
    def __init__(self, purchase_id, stock_ticker, stock_date, stock_open, stock_high, stock_low, stock_close, stock_adj_close, stock_volume):
        #assign some values based on what was passed to the class
        self.ticker = stock_ticker
        self.date = stock_date
        self.open = stock_open
        self.high = stock_high
        self.low = stock_low
        self.close = stock_close
        self.adj_close = stock_adj_close
        self.volume = stock_volume
        

if __name__ ==  "__main__":


    #create the database file and tables if they don't already exist
    db_location = "./"
    db_file = "mod_7.db"

    try:
        conn = sqlite3.connect(db_location+db_file)
    except:
        print("Failed to connect to database.")

    cursor = conn.cursor()

    #delete the old tables
    sql_query = "DROP TABLE If EXISTS stockdata"
    cursor.execute(sql_query)

    #create the table
    sql_query = "CREATE TABLE IF NOT EXISTS 'stockdata' ('data_id' INTEGER UNIQUE, 'investor_id' INTEGER, 'symbol' text, 'purchase_date' TEXT, 'open' NUMERIC, 'high' NUMERIC, 'low' NUMERIC, 'close' NUMERIC, 'volume' INTEGER, PRIMARY KEY ('data_id' AUTOINCREMENT));"
    cursor.execute(sql_query)

    #locate the files to load
    #define the path from this file to the stored data
    file_path="c:/DU Python/4370/stockdata/"

    #use list comprehension and a filter to only pull the .csv files from the directory
    #drop the last 4 characters of each list to get just the filename without the extension
    files = [f[:-4] for f in os.listdir(file_path) if f.endswith('.csv')]
    print(files)

    #make an investor that will hold all the stock data from the csv files
    my_investor = Investor(1, "Bob", "123 Technology Way")
    
    #read all the CSV files 
    for filename in files:
    #read the data from the appropriate csv and create stock objects for each.
        try:
            #with will auto-release the file connection
            with open(f"{file_path}{filename}.csv", "r") as file:
                
                #read the header to a separate variable
                data_header = file.readline()

                #split up the values of the header line, stripping white space
                header_split=data_header.strip().split(",")
               
                #find the indicies for each column
                date_index = header_split.index("Date")
                open_index = header_split.index("Open")
                high_index = header_split.index("High")
                low_index = header_split.index("Low")
                close_index = header_split.index("Close")
                adj_close_index = header_split.index("Adj Close")
                volume_index = header_split.index("Volume")

                #read the rest of the data from the file, count how many times this is done
                for count, line in enumerate(file):
                    #split up the line, stripping whitespace
                    line_split= line.strip().split(",")
                    #call the method to add a new stock
                    my_investor.add_stockdata(count, filename, line_split[date_index], 
                                        line_split[open_index], line_split[high_index], 
                                        line_split[low_index], line_split[close_index],
                                         line_split[adj_close_index], line_split[volume_index] )
                
        except:
           print('Unable to read stockdata/'+filename+'.csv')

    #create a dataframe of the stockdata objects
    df = my_investor.pandafy_stocks()

    #loop over the values and insert these into the database
    for index, row in df.iterrows():
        #insert the data into the database
        sql_query = f"""INSERT INTO stockdata (investor_id, symbol, purchase_date, close) 
        VALUES ({my_investor.investor_id}, '{row["ticker"]}','{row["date"]}', '{row["close"]}');"""
        #print(sql_query)
        cursor.execute(sql_query)

    #load all the data into the database
 
    #do some manipulation

    #make a graph


    #done with the database now
    conn.commit()
    conn.close()
