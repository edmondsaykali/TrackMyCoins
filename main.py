import sys
import os
import requests
from datetime import date
import exceptions


numOfCoins = int(
    input('Please input how many coins would you like to track : '))
coinDict = {}
fCoinDict = {}


def append_value(dict_obj, key, value):
    if key in dict_obj:
        raise exceptions.KeyExists
    else:
        dict_obj[key] = value


for _ in range(numOfCoins):
    coinName = input('Please input the name of the coin : ')
    if isinstance(coinName, str) == False:
        raise exceptions.KeyExists
    coinTotal = float(input('Please input how much '+coinName+' you own : '))
    append_value(coinDict, coinName, coinTotal)

try:
    for key, value in coinDict.items():
        url = 'https://api.nomics.com/v1/currencies/ticker?key=b24db6b794a971ab4caecfe738d3872a&ids=' + \
            str(key)+'&interval=1h,30d&convert=USD&per-page=100&page=1'
        req = requests.get(url)

        if req.status_code != 200:
            raise exceptions.RequestError
        if not req.json():
            raise exceptions.coinNotAvailable
        for x in req.json():
            coinPrice = float(x['price'])

        totalAssets = float(value)*coinPrice
        fCoinDict[str(key)] = totalAssets
        today = date.today()
        dat = today.strftime("%d/%m/%y")

except exceptions.RequestError:
    print("\nError has occured while raising the request")
    sys.exit(1)
except exceptions.coinNotAvailable:
    print("\nSorry! The coin you specified could not be found")
    sys.exit(1)
except exceptions.KeyExists:
    print("\nSorry! Please enter a valid coin name")
    sys.exit(1)

print('\n\n##Your Wallet \n')
sum=0
for key, value in fCoinDict.items():
    print(str(key)+' : $'+str(value))
    sum+=value
print('\n\nTotal Networth : $'+str(sum))
