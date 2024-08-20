"""
Jacob Ezzell
June 22th 2024
ICS 4370
Description: This loops over a list and calculates a value for each set of items in the list
"""

#prep the lists
stocks = ['GOOGLE','MSFT', 'RDS-A', 'AIG', 'FB']
shares = [25, 85, 400, 235, 130]
purchasedAt = [772.88, 56.60, 49.58, 54.21, 124.31]
currentValue = [941.53, 73.04, 55.74, 65.27, 175.45]
earnLoss = [] #starts empty, will get the values during the loop
earnLossPerStock = [] #starts empty, will get the values during the loop

#formatting line length
lineLength = 30

#print the header
print('-' * lineLength)
print('Stock Summary for Jacob:')
print('-' * lineLength)

#i is my iterator variable
i = 0
#maxChange is the pointer to the stock that earned or lost the most
maxChange = 0
#maxValue is the pointer to the stock with the per-share change
maxValue = 0

#for each stock in the list
while i< len(stocks):
    #calculate the earning/loss
    earnLossPerStock.append((currentValue[i] - purchasedAt[i]))
    earnLoss.append(earnLossPerStock[i] * shares[i])
    
    #print the row
    print(f"|{stocks[i]:^10}|{shares[i]:^6}|{earnLoss[i]:^10.2f}|")
    #test if the total change is the biggest one yet
    if(abs(earnLoss[i]) > abs(earnLoss[maxChange])):
        #if not, assign the pointer the new max position
        maxChange = i
    #test if this stock had the largest per-share change
    if(abs(earnLossPerStock[i]) > abs(earnLossPerStock[maxValue])):
        #if not, assign the pointer the new max position
        maxValue = i

    #last step, increment the iterator
    i +=1

#was it a gain or loss?
if earnLoss[maxChange] > 0:
    gainLoss = "gained"
else:
    gainLoss = "lost"


#print out the footer with the biggest values
print('-' * lineLength)
print(f"The stock with the largest change \nis {stocks[maxChange]} which \n{gainLoss} ${earnLoss[maxChange]:.2f}.")
print('-' * lineLength)

#was it a gain or loss?
if earnLossPerStock[maxValue] > 0:
    gainLossPerStock = "gained"
else:
    gainLossPerStock = "lost"

#print out the footer with the biggest per-stock change
print(f"The stock with the largest per-stock change\nis {stocks[maxValue]} which \n{gainLossPerStock} ${earnLoss[maxValue]:.2f}.")
print('-' * lineLength)

