"""
Jacob Ezzell
July 30th 2024
ICS 4370
Description: create a set of nested classes with attributes and methods to work with stock and bond data
            read data in from a file, write to a database, read from the database, and then populate some objects.

"""
from datetime import date, datetime
from prettytable import PrettyTable
import sqlite3

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
    sql_query = "DROP TABLE If EXISTS investors"
    cursor.execute(sql_query)
    sql_query = "DROP TABLE If EXISTS stocks"
    cursor.execute(sql_query)
    sql_query = "DROP TABLE If EXISTS bonds"
    cursor.execute(sql_query)

    #create the database structure
    sql_query = "CREATE TABLE IF NOT EXISTS investors (investor_id INTEGER PRIMARY KEY, name TEXT, address TEXT);"
    cursor.execute(sql_query)
    sql_query = "CREATE TABLE IF NOT EXISTS 'stocks' ('stock_id' INTEGER UNIQUE, 'investor_id' INTEGER, 'symbol' text, 'no_shares' INTEGER, 'purchase_price' NUMERIC, 'current_value' NUMERIC, 'purchase_date' TEXT, PRIMARY KEY ('stock_id' AUTOINCREMENT));"
    cursor.execute(sql_query)
    sql_query = "CREATE TABLE IF NOT EXISTS 'bonds' ('bond_id' INTEGER UNIQUE, 'investor_id' INTEGER, 'symbol' text, 'no_shares' INTEGER, 'purchase_price' NUMERIC, 'current_value' NUMERIC, 'purchase_date' TEXT, 'coupon' NUMERIC, 'yield' NUMERIC, PRIMARY KEY ('bond_id' AUTOINCREMENT));"
    cursor.execute(sql_query)

    #data files to load into the database
    stock_file = "Lesson6_Data_Stocks.csv"
    bond_file = "Lesson6_Data_Bonds.csv"

    #make an investor
    my_investor = Investor(1, "Bob", "123 Technology Way")

    #insert the investor into the table
    sql_query = f"INSERT INTO investors (investor_id, name, address) VALUES ({my_investor.investor_id}, '{my_investor.name}','{my_investor.address}');"
    #print(sql_query)
    cursor.execute(sql_query)
    

    #open link to the stock file and read in the values
    #try opening the file
    try:
        #with will auto-release the file connection
        with open(stock_file, "r") as file:
            
            #read the header to a separate variable
            data_header = file.readline()

            #split up the values of the header line, stripping white space
            header_split=data_header.strip().split(",")
            
            #find the indicies for each column
            ticker_index = header_split.index("SYMBOL")
            shares_index = header_split.index("NO_SHARES")
            purchased_at_index = header_split.index("PURCHASE_PRICE")
            current_value_index = header_split.index("CURRENT_VALUE")
            purchase_date_index = header_split.index("PURCHASE_DATE")

            #read the rest of the data from the file, count how many times this is done
            for count, line in enumerate(file):
                #split up the line, stripping whitespace
                line_split= line.strip().split(",")
                
                #insert the stock into the database
                sql_query = f"""INSERT INTO stocks (investor_id, symbol, no_shares, purchase_price, current_value, purchase_date) 
                VALUES ({my_investor.investor_id}, '{line_split[ticker_index]}',{line_split[shares_index]},{line_split[purchased_at_index]},{line_split[current_value_index]},'{line_split[purchase_date_index]}');"""
                #print(sql_query)
                cursor.execute(sql_query)

            #now get the information from the database and populate the structure
            sql_query = "SELECT investor_id, symbol, no_shares, purchase_price, current_value, purchase_date FROM stocks;"
            #print(sql_query)
            cursor.execute(sql_query)
            
            stocks = cursor.fetchall()
            for count, stock in enumerate(stocks):
                #call the method to add a new stock
                my_investor.add_stock(count, stock[1], stock[2],stock[3], stock[4],stock[5])

            #find the largest stock
            biggest_stock = my_investor.biggest_stock()

            #put the stocks in a table
            table = PrettyTable()

            #load the names of the columns into the table object
            table.field_names=["Ticker", "Shares", "Earn/Loss Total", "Earn/Loss Rate"]

            #Pass the table to the method to fill up.
            my_investor.get_stocks(table)

            table.title = f"Summary for {my_investor.name}'s Stock Database"
            print(table)
            
    except(FileNotFoundError):
        print("error opening file")


#
##
###BONDS
##
#

    #open link to the bond file and read in the values
    #try opening the file
    try:
        #with will auto-release the file connection
        with open(bond_file, "r") as file:
            
            #read the header to a separate variable
            data_header = file.readline()

            #split up the values of the header line, stripping white space
            header_split=data_header.strip().split(",")
            
            #find the indicies for each column
            ticker_index = header_split.index("SYMBOL")
            shares_index = header_split.index("NO_SHARES")
            purchased_at_index = header_split.index("PURCHASE_PRICE")
            current_value_index = header_split.index("CURRENT_VALUE")
            purchase_date_index = header_split.index("PURCHASE_DATE")
            coupon_index = header_split.index("Coupon")
            yield_index = header_split.index("Yield")

            #read the rest of the data from the file, count how many times this is done
            for count, line in enumerate(file):
                #split up the line, stripping whitespace
                line_split= line.strip().split(",")
                
                #insert the bond into the database
                sql_query = f"""INSERT INTO bonds (investor_id, symbol, no_shares, purchase_price, current_value, purchase_date, coupon, yield) 
                VALUES ({my_investor.investor_id}, '{line_split[ticker_index]}',{line_split[shares_index]},{line_split[purchased_at_index]},{line_split[current_value_index]},'{line_split[purchase_date_index]}','{line_split[coupon_index]}','{line_split[yield_index]}');"""
                #print(sql_query)
                cursor.execute(sql_query)           
            
            
            #now get the information from the database and populate the structure
            sql_query = "SELECT investor_id, symbol, no_shares, purchase_price, current_value, purchase_date, coupon, yield FROM bonds;"
            #print(sql_query)
            cursor.execute(sql_query)
            
            bonds = cursor.fetchall()
            for count, bond in enumerate(bonds):
                #call the method to add a new bond
                my_investor.add_bond(count, bond[1], bond[2],bond[3], bond[4],bond[5],bond[6],bond[7])
            
            
            #find the largest bond
            biggest_bond = my_investor.biggest_bond()

            #put the bonds in a table
            table = PrettyTable()

            #load the names of the columns into the table object
            table.field_names=["Ticker", "Shares", "Coupon", "Yield", "Earn/Loss Total", "Earn/Loss Rate"]

            #Pass the table to the method to fill up.
            my_investor.get_bonds(table)

            table.title = f"Summary for {my_investor.name}'s Bond Database"
            print(table)

    except(FileNotFoundError):
        print("error opening file")

    

    conn.commit()
    conn.close()
