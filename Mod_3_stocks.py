"""
Jacob Ezzell
July 3rd 2024
ICS 4370
Description: This loops over a dictionary and calculates a value for each set of items in the list, then finds the maximums
"""

#prep the dictionary. Since the stock ticker codes are all unique, I can use this for the main dictionary key
stocks = {'GOOGLE' : {'shares':25, 'purchasedAt':772.88, 'currentValue':941.53}}
stocks['MSFT'] = {'shares':85, 'purchasedAt':56.60, 'currentValue':73.04}
stocks['RDS-A'] = {'shares':400, 'purchasedAt':49.58, 'currentValue':55.74}
stocks['AIG'] = {'shares':235, 'purchasedAt':54.21, 'currentValue':65.27}
stocks['FB'] = {'shares':130, 'purchasedAt':124.31, 'currentValue':175.45}

#formatting line length
lineLength = 30

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
    
    #calculate the earning/loss
    stocks[stock]['earnLossPerShare'] = stocks[stock]['currentValue'] - stocks[stock]['purchasedAt'] 
    stocks[stock]['earnLoss'] = stocks[stock]['earnLossPerShare'] * stocks[stock]['shares'] 

    #print the row
    print(f"|{stock:^10}|{stocks[stock]['shares']:^6}|{stocks[stock]['earnLoss']:^10.2f}|")

    #is this the biggest one?
    #if it's still blank, start here
    if(maxELStock==''):
        maxELStock = stock
    elif(abs(stocks[maxELStock]['earnLoss']) < abs(stocks[stock]['earnLoss'])):
        maxELStock = stock

    #also check the 'per stock' max
    if(maxELPerShare==''):
        maxELPerShare = stock
    elif(abs(stocks[maxELPerShare]['earnLossPerShare']) < abs(stocks[stock]['earnLossPerShare'])):
        maxELPerShare = stock
    
# uncomment these for testing if needed
# print(maxELStock)
# print(maxELPerShare)
 
#was it a gain or loss?
if (stocks[maxELStock]['earnLoss']) > 0:
    gainLoss = "gained"
else:
    gainLoss = "lost"

#print out the footer with the biggest values
print('-' * lineLength)
print(f"The stock with the largest \noverall change is \n{maxELStock} which \n{gainLoss} ${stocks[maxELStock]['earnLoss']:.2f}.")
print('-' * lineLength)

#was it a gain or loss?
if (stocks[maxELPerShare]['earnLoss']) > 0:
    gainLoss = "gained"
else:
    gainLoss = "lost"

#print out the footer with the biggest values
print(f"The stock with the largest \nchange per share is \n{maxELPerShare} which \n{gainLoss} ${stocks[maxELStock]['earnLoss']:.2f}.")
print('-' * lineLength)

