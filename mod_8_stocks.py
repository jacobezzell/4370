"""
Jacob Ezzell
August 8th 2024
ICS 4370
Description: display stock data from a json file
"""
from datetime import date, datetime
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sqlite3
import json

#import the class file from last week
from mod_6_stocks import *

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
    #sql_query = "DROP TABLE If EXISTS stockdata"
    #cursor.execute(sql_query)

    #sql_query = "CREATE TABLE IF NOT EXISTS 'stockdata' ('data_id' INTEGER UNIQUE, 'symbol' text, 'purchase_date' TEXT, 'open' NUMERIC, 'high' NUMERIC, 'low' NUMERIC, 'close' NUMERIC, 'volume' INTEGER, PRIMARY KEY ('data_id' AUTOINCREMENT));"
    #cursor.execute(sql_query)
   
    #make an investor
    my_investor = Investor(1, "Bob", "123 Technology Way")

    
    #load all the stock data from the json
    file_path = 'AllStocks.json'
    with open(file_path) as json_file:
        data_set = json.load(json_file)

    #load all the data into the database
    for count, data in enumerate(data_set):
        #insert the stock into the database
        sql_query = f"""INSERT INTO stockdata (data_id, symbol, purchase_date, open, high, low, close, volume) 
        VALUES ({count}, '{data["Symbol"]}', '{data["Date"]}', '{data["Open"]}', '{data["High"]}', '{data["Low"]}', '{data["Close"]}', '{data["Volume"]}');"""
        #cursor.execute(sql_query)

   
    #now get the information from the database and populate the structure
    sql_query = "SELECT investor_id, symbol, no_shares, purchase_price, current_value, purchase_date FROM stocks;"
    cursor.execute(sql_query)
    
    stocks = cursor.fetchall()
    for count, stock in enumerate(stocks):
        #call the method to add a new stock
        my_investor.add_stock(count, stock[1], stock[2],stock[3], stock[4],stock[5])

    #create a plot. the ax object is needed to nicely label the axis
    fig, ax = plt.subplots()

    #for each of the investor's stocks
    for stock in my_investor.stocks:
        #print(f"{stock.ticker}")
        #find all the stock data for that stock
        sql_query = f"SELECT data_id, symbol, purchase_date, close FROM stockdata WHERE symbol LIKE '{stock.ticker}';"
        #print(sql_query)
        cursor.execute(sql_query)
        allstockdata = cursor.fetchall()

        #empty lists to hold the stock values
        x_dates = []
        y_values = []
        for stockdata in allstockdata:
            #multiply each day's close by the number of shares purchased
            net_value = stock.shares * stockdata[3]
            #create a datetime object out of the stored date
            net_date = datetime.strptime(stockdata[2], "%d-%b-%y").date()
            #make a list of X and Y values for that stock and put those in lists
            x_dates.append(net_date)
            y_values.append(net_value)

        #create a line with this set of X and Y values
        ax.plot(x_dates, y_values, label=stock.ticker)

    #done with the database now
    conn.commit()
    conn.close()

    # Format the x-axis for dates
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.grid(True)  # Add grid lines for better readability

    # Set labels and title
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Line Plot (Stock Values)')

    #formatting the figure
    fig.set_figwidth(10) 
    fig.set_figheight(5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()

    plt.savefig("stockdisplay.png")
    plt.show()

    