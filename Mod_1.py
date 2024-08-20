"""
Jacob Ezzell
June 17th 2024
ICS 4370
Description: This code will get several inputs from the user, do a simple calculation, then output a result
"""

#get all the inputs
userName = input("Enter your name:")
stockName = input("Enter the name of your stock:")
stockPriceStart = input("Enter the price of the stock when you bought it:")
stockShares = input("Enter the number of shares you bought:")
stockPriceEnd = input("Enter current price of the stock:")
profitLoss = (float(stockPriceEnd) - float(stockPriceStart)) * float(stockShares)

#print the output, with some new lines and tabs to make things line up better
print(f"\n\n========================\n")
print(f"Stock summary for:\t{userName}")

#format the stock name in uppercase
print(f"{stockName.upper()}:\t\t\t{stockShares} shares")
print(f"Purchase price:\t\t{stockPriceStart}")
print(f"Current price:\t\t{stockPriceEnd}")

#format the profit/loss with two decimal places
print(f"Profit/Loss to date:\t${profitLoss:.2f}")
print("========================")