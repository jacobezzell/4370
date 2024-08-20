"""
Jacob Ezzell
July 12th 2024
ICS 4370
Description: This loops over a dictionary and calculates a value 
for each set of items in the list, then finds the maximums. 
This version uses functions to calculate all the values
"""
from datetime import date, datetime

def earn_loss_per_share(cur_val, purch_at):
    """calculate the earning/loss per share"""
    return (cur_val - purch_at)

def earn_loss_total(e_l_p_s, shares):
    """calculate the total change for all shares of the stock"""
    return (e_l_p_s * shares)

def earn_loss_rate(e_l_p_s, purch_at, purch_date):
    """
    calculate the approximate annual rate of change using this formula:
    ((((current value - purchase price)/purchase price)/(current date – purchase date)))*100
    (cur val - purch price) was already calculated, and passed as a single value here as e_l_p_s
    """
    cur_date = date.today()
    pur_date = datetime.strptime(purch_date, '%m/%d/%Y').date()
    days = (cur_date - pur_date).days 
    return (e_l_p_s / purch_at / days * 100)
    


#prep the dictionary. Since the stock ticker codes are all unique, I can use this for the main dictionary key
stocks = {'GOOGLE' : {'shares':25, 'purchased_at':772.88, 'current_value':941.53, 'purchase_date':'8/1/2017'}}
stocks['MSFT'] = {'shares':85, 'purchased_at':56.60, 'current_value':73.04, 'purchase_date':'8/1/2017'}
stocks['RDS-A'] = {'shares':400, 'purchased_at':49.58, 'current_value':55.74, 'purchase_date':'8/1/2017'}
stocks['AIG'] = {'shares':235, 'purchased_at':54.21, 'current_value':65.27, 'purchase_date':'8/1/2017'}
stocks['FB'] = {'shares':130, 'purchased_at':124.31, 'current_value':175.45, 'purchase_date':'8/1/2017'}
stocks['M'] =  {'shares':425, 'purchased_at':30.30, 'current_value':23.98, 'purchase_date':'1/10/2018'}
stocks['F'] =  {'shares':85, 'purchased_at':12.58, 'current_value':10.95, 'purchase_date':'2/17/2018'}
stocks['IBM'] =  {'shares':80, 'purchased_at':150.37, 'current_value':145.30, 'purchase_date':'5/12/2018'}

#formatting line length
lineLength = 40

#print the header
print('-' * lineLength)
print('Stock Summary for Jacob:')
print('-' * lineLength)

#pointers to track max stock changes
maxELStock = ''
maxELPerShare = ''

#for each stock in the list
for stock in stocks:
    #print(stocks[stock])
    
    #calculate the earning/loss per share
    stocks[stock]['earn_loss_per_share'] = earn_loss_per_share(stocks[stock]['current_value'], stocks[stock]['purchased_at']) 
    
    #calculate the earn/loss for the whole stock.
    stocks[stock]['earn_loss'] = earn_loss_total(stocks[stock]['earn_loss_per_share'], stocks[stock]['shares']) 
    
    #calculate yearly earning loss rate
    stocks[stock]['earn_loss_rate'] = earn_loss_rate(stocks[stock]['earn_loss_per_share'], stocks[stock]['purchased_at'], stocks[stock]['purchase_date'] )


    #print the row
    print(f"|{stock:^10}|{stocks[stock]['shares']:^6}|{stocks[stock]['earn_loss']:^10.2f}|{stocks[stock]['earn_loss_rate']:^10.2%}|")

    #is this the biggest one?
    #if it's still blank, start here
    if(maxELStock==''):
        maxELStock = stock
    elif(abs(stocks[maxELStock]['earn_loss']) < abs(stocks[stock]['earn_loss'])):
        maxELStock = stock

    #also check the 'per stock' max
    if(maxELPerShare==''):
        maxELPerShare = stock
    elif(abs(stocks[maxELPerShare]['earn_loss_per_share']) < abs(stocks[stock]['earn_loss_per_share'])):
        maxELPerShare = stock
    
# uncomment these for testing if needed
# print(maxELStock)
# print(maxELPerShare)
 
#was it a gain or loss?
if (stocks[maxELStock]['earn_loss']) > 0:
    gainLoss = "gained"
else:
    gainLoss = "lost"

#print out the footer with the biggest values
print('-' * lineLength)
print(f"The stock with the largest \noverall change is \n{maxELStock} which \n{gainLoss} ${stocks[maxELStock]['earn_loss']:.2f}.")
print('-' * lineLength)

#was it a gain or loss?
if (stocks[maxELPerShare]['earn_loss']) > 0:
    gainLoss = "gained"
else:
    gainLoss = "lost"

#print out the footer with the biggest values
print(f"The stock with the largest \nchange per share is \n{maxELPerShare} which \n{gainLoss} ${stocks[maxELPerShare]['earn_loss']:.2f}.")
print('-' * lineLength)

