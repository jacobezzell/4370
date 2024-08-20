"""
Jacob Ezzell
July 29th 2024
ICS 4370
Description: interface the stocks and bonds with a SQLite database.

"""
from datetime import date, datetime
from prettytable import PrettyTable

#define an investor class
class Investor:
    def __init__(self, investor_id, name, address):
        self.investor_id = investor_id
        self.name = name
        self.address = address
        #lists to contain the investor's stocks and bonds
        self.stocks = []
        self.bonds = []
        #pointers to the largest stock and bond in the lists
        self.max_e_l_stock = 0
        self.max_e_l_bond = 0
    
    def add_stock(self, purchase_id, ticker, shares, purchased_at, current_value, purchase_date):
        new_stock = Stock(purchase_id, ticker, shares, purchased_at, current_value, purchase_date)
        self.stocks.append(new_stock)

    def add_bond(self, purchase_id, ticker, shares, purchased_at, current_value, purchase_date, coupon, yield_rate):
        new_bond = Bond(purchase_id, ticker, shares, purchased_at, current_value, purchase_date, coupon, yield_rate)
        self.bonds.append(new_bond)

    def biggest_stock(self):
        for counter, stock in enumerate(self.stocks):
            #is this the biggest one?
            if(abs(self.stocks[self.max_e_l_stock].earn_loss_total) < abs(stock.earn_loss_total)):
                self.max_e_l_stock = counter
        return(self.stocks[self.max_e_l_stock].ticker)

    def biggest_bond(self):
        for counter, bond in enumerate(self.bonds):
            #is this the biggest one?
            if(abs(self.bonds[self.max_e_l_bond].earn_loss_total) < abs(bond.earn_loss_total)):
                self.max_e_l_bond = counter
        return(self.bonds[self.max_e_l_bond].ticker)

    def get_stocks(self, table):
        for stock in self.stocks:
            #put the values into the table
            table.add_row([stock.ticker, stock.shares, round(stock.earn_loss_total,2), round(stock.earn_loss_rate,2)])
           
    def get_bonds(self, table):
        for bond in self.bonds:
            #put the values into the table
            table.add_row([bond.ticker, bond.shares, bond.coupon, bond.yield_rate, round(bond.earn_loss_total,2), round(bond.earn_loss_rate,2)])

#define the stock class:
class Stock:
    def __init__(self, purchase_id, ticker, shares, purchased_at, current_value, purchase_date):
        #assign some values based on what was passed to the class
        self.ticker = ticker
        # force the values to be an int since its a string
        try:
            self.shares = int(shares)
        except:
            print(f"Share value is not an integer:{shares}")
            raise SystemExit("Exiting program")
        
        # force the values to be a float since its a string
        try:
            self.purchased_at = float(purchased_at)
        except:
            print(f"Purchase value is not a float:{purchased_at}")
            raise SystemExit("Exiting program")
    
        try:
            self.current_value = float(current_value)
        except:
            print(f"Current value is not a float:{current_value}")
            raise SystemExit("Exiting program")

        self.purchase_date = purchase_date
        #the earn/loss values can be calculated at initiation since we have all the information we needed
        self.earn_loss_per_share = self.current_value - self.purchased_at 
        self.earn_loss_total = self.earn_loss_per_share * self.shares
        """
        calculate the approximate annual rate of change using this formula:
        ((((current value - purchase price)/purchase price)/(current date – purchase date)))*100
        (cur val - purch price) was already calculated, and passed as a single value here as e_l_p_s
        """
        try:
            cur_date = date.today()
            pur_date = datetime.strptime(self.purchase_date, "%m/%d/%Y").date()
            days = (cur_date - pur_date).days 
            self.earn_loss_rate = (self.earn_loss_per_share / self.purchased_at / days * 100)
        except:
            print(f"Unable to calculate Earn/Loss, check date:{purchase_date}")
            raise SystemExit("Exiting program")

#define the bond class as an extension of Stock
class Bond(Stock):
    #override the initialization function, and the variable that should be passed to the class
    def __init__(self, purchase_id, ticker, shares, purchased_at, current_value, purchase_date, coupon, yield_rate):

        #use Super() to call the initialization method from the parent class of "stock" so we don't have to do that again
        super().__init__(purchase_id, ticker, shares, purchased_at, current_value, purchase_date)
        
        #assign the extra two values
        
        # force the values to be a float since its a string
        try:
            self.coupon = float(coupon)
        except:
            print(f"Coupon value is not a float:{coupon}")
            raise SystemExit("Exiting program")
        
        try:
            self.yield_rate = yield_rate
        except:
            print(f"Yield Rate is not a float:{yield_rate}")
            raise SystemExit("Exiting program")
        

if __name__ ==  "__main__":
    stock_file = "Lesson6_Data_Stocks.csv"
    bond_file = "Lesson6_Data_Bonds.csv"

    #make an investor
    my_investor = Investor(1, "Bob", "123 Technology Way")

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
                #call the method to add a new stock
                my_investor.add_stock(count, line_split[ticker_index], line_split[shares_index], 
                                    line_split[purchased_at_index], line_split[current_value_index], 
                                    line_split[purchase_date_index])
            
            
    except(FileNotFoundError):
        print("error opening file")

    #find the largest stock
    biggest_stock = my_investor.biggest_stock()

    #put the stocks in a table
    table = PrettyTable()

    #load the names of the columns into the table object
    table.field_names=["Ticker", "Shares", "Earn/Loss Total", "Earn/Loss Rate"]

    #Pass the table to the method to fill up.
    my_investor.get_stocks(table)

    table.title = f"Stock Summary for {my_investor.name}"
    #print(table)

    #dump the results to a file
    try:
        #with will auto-release the file connection
        with open("results.txt", "w") as file:
            #dump the table to the file, but make it a string via the get_string method.
            file.write(table.get_string())
 
            #was it a gain or loss?
            if (my_investor.stocks[my_investor.max_e_l_stock].earn_loss_total) > 0:
                gainLoss = "gained"
            else:
                gainLoss = "lost"

            #print out the footer with the biggest values
            file.write(f"\nThe stock with the largest overall change is {my_investor.stocks[my_investor.max_e_l_stock].ticker} which \n{gainLoss} ${my_investor.stocks[my_investor.max_e_l_stock].earn_loss_total:.2f}.\n")
            
    except(FileNotFoundError):
        print("error opening stock file")

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
                #call the method to add a new stock
                my_investor.add_bond(count, line_split[ticker_index], line_split[shares_index], 
                                    line_split[purchased_at_index], line_split[current_value_index], 
                                    line_split[purchase_date_index], line_split[coupon_index], line_split[yield_index])
            
            
    except(FileNotFoundError):
        print("error opening file")

    #find the largest stock
    biggest_bond = my_investor.biggest_bond()

    #put the bonds in a table
    table = PrettyTable()

    #load the names of the columns into the table object
    table.field_names=["Ticker", "Shares", "Coupon", "Yield", "Earn/Loss Total", "Earn/Loss Rate"]

    #Pass the table to the method to fill up.
    my_investor.get_bonds(table)

    table.title = f"Bond Summary for {my_investor.name}"
    #print(table)

    #dump the results to a file, but append it this time
    try:
        #with will auto-release the file connection
        with open("results.txt", "a") as file:
            #dump the table to the file, but make it a string via the get_string method.
            file.write(table.get_string())

            #was it a gain or loss?
            if (my_investor.bonds[my_investor.max_e_l_bond].earn_loss_total) > 0:
                gainLoss = "gained"
            else:
                gainLoss = "lost"

            #print out the footer with the biggest values
            file.write(f"\nThe bond with the largest overall change is {my_investor.bonds[my_investor.max_e_l_bond].ticker} which \n{gainLoss} ${my_investor.bonds[my_investor.max_e_l_bond].earn_loss_total:.2f}.\n")

    except(FileNotFoundError):
        print("error opening bond file")

