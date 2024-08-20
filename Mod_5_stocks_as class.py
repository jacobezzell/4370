"""
Jacob Ezzell
July 17th 2024
ICS 4370
Description: create a class with attributes and methods to work with stock data
"""
from datetime import date, datetime


#define an investor class
class Investor:
    def __init__(self, investor_id, name, address):
        self.name = name
        self.address = address

#define the stock class:
class Stock:
    def __init__(self, purchase_id, ticker, shares, purchased_at, current_value, purchase_date):
        #assign some values based on what was passed to the class
        self.ticker = ticker
        self.shares = shares
        self.purchased_at = purchased_at
        self.current_value = current_value
        self.purchase_date = purchase_date

        #the earn/loss values can be calculated at initiation since we have all the information we needed
        self.earn_loss_per_share = current_value - purchased_at 
        self.earn_loss_total = self.earn_loss_per_share * shares


    def earn_loss_rate(self):
        """
        calculate the approximate annual rate of change using this formula:
        ((((current value - purchase price)/purchase price)/(current date – purchase date)))*100
        (cur val - purch price) was already calculated, and passed as a single value here as e_l_p_s
        """
        cur_date = date.today()
        pur_date = datetime.strptime(self.purchase_date, '%m/%d/%Y').date()
        days = (cur_date - pur_date).days 
        self.earn_loss_rate = (self.earn_loss_per_share / self.purchased_at / days * 100)


#define the bond class as an extension of Stock
class Bond(Stock):
    #override the initialization function, and the variable that should be passed to the class
    def __init__(self, purchase_id, ticker, shares, purchased_at, current_value, purchase_date, coupon, yield_rate):

        #use Super() to call the initialization method from the parent class of "stock" so we don't have to do that again
        super().__init__(purchase_id, ticker, shares, purchased_at, current_value, purchase_date)
        
        #assign the extra two values
        self.coupon = coupon
        self.yield_rate = yield_rate


#empty list variable to contain the stock objects
my_stocks = []
#prep a list of stocks, using the ticker name for each instance
my_stocks.append(Stock(1, 'GOOGLE', 25, 772.88, 941.53, '8/1/2017'))
my_stocks.append(Stock(2, 'MSFT', 85, 56.60, 73.04, '8/1/2017'))
my_stocks.append(Stock(3, 'RDS-A', 400, 49.58, 55.74, '8/1/2017'))
my_stocks.append(Stock(4, 'AIG', 235,54.21, 65.27, '8/1/2017'))
my_stocks.append(Stock(5, 'FB', 130, 124.31, 175.45, '8/1/2017'))
my_stocks.append(Stock(6, 'M', 425,30.30, 23.98, '1/10/2018'))
my_stocks.append(Stock(7, 'F', 85, 12.58, 10.95, '2/17/2018'))
my_stocks.append(Stock(8, 'IBM', 150.37, 145.30, 145.30, '5/12/2018'))

my_bonds=[Bond(1, 'GT2:GOV', 200, 100.02, 100.05, '8/1/2017', 1.38, 1.35)]

my_investor = Investor(1, 'Bob', '123 Technology Way')

#formatting line length
lineLength = 40

#print the header
print('-' * lineLength)
print(f'Stock Summary for {my_investor.name}:')
print('-' * lineLength)
print(f"|{'Ticker':^10}|{'Shares':^6}|{'Earn/Loss':^10}|{'E/L Rate':^10}|")
print('-' * lineLength)

#pointers to track max stock changes
maxELStock = 0

#pointer to keep track of which stock im at in the list while looping
i = 0

#loop over the list of stocks and do some things to each one.
for stock in my_stocks:
    #test output for debugging objects
    #print(f"{stock.ticker} = {stock.shares}")
    
    #calculate yearly earning loss rate
    stock.earn_loss_rate()

    #print the row
    print(f"|{stock.ticker:^10}|{stock.shares:^6}|{stock.earn_loss_total:^10.2f}|{stock.earn_loss_rate:^10.2%}|")

    #is this the biggest one?
    if(abs(my_stocks[maxELStock].earn_loss_total) < abs(stock.earn_loss_total)):
        maxELStock = i
    
    #last thing, iterate up the counter
    i += 1

# uncomment these for testing if needed
#print(my_stocks[maxELstock].ticker)
# print(maxELPerShare)
 
#was it a gain or loss?
if (my_stocks[maxELStock].earn_loss_total) > 0:
    gainLoss = "gained"
else:
    gainLoss = "lost"

#print out the footer with the biggest values
print('-' * lineLength)
print(f"The stock with the largest \noverall change is \n{my_stocks[maxELStock].ticker} which \n{gainLoss} ${my_stocks[maxELStock].earn_loss_total:.2f}.")
print('-' * lineLength)

"""
Now do it all over again for the bonds
"""

#formatting line length
lineLength = 54
#reset the pointer for the bond loop
i = 0
maxELBond = 0


#print the header
print('-' * lineLength)
print(f'Bond Summary for {my_investor.name}:')
print('-' * lineLength)
print(f"|{'Ticker':^10}|{'Shares':^6}|{'Coupon':^6}|{'Yld R':^6}|{'Earn/Loss':^10}|{'E/L Rate':^10}|")
print('-' * lineLength)

#loop over the list of bonds and do some things to each one.
for bond in my_bonds:
    #test output for debugging objects
    #print(f"{bond.ticker} = {bond.shares}")
    
    #calculate yearly earning loss rate
    bond.earn_loss_rate()

    #print the row
    print(f"|{bond.ticker:^10}|{bond.shares:^6}|{bond.coupon:^6}|{bond.yield_rate:^6}|{bond.earn_loss_total:^10.2f}|{bond.earn_loss_rate:^10.2%}|")

    #is this the biggest one?
    if(abs(my_bonds[maxELBond].earn_loss_total) < abs(bond.earn_loss_total)):
        maxELbond = i
    
    #last thing, iterate up the counter
    i += 1

#was it a gain or loss?
if (my_bonds[maxELBond].earn_loss_total) > 0:
    gainLoss = "gained"
else:
    gainLoss = "lost"

#print out the footer with the biggest values
print('-' * lineLength)
print(f"The bond with the largest \noverall change is \n{my_bonds[maxELBond].ticker} which \n{gainLoss} ${my_bonds[maxELBond].earn_loss_total:.2f}.")
print('-' * lineLength)




