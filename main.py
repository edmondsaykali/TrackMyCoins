import sys
import os
import requests
from datetime import date
import exceptions


coin = input('Please input the name of the coin : ')
coinAsset = float(input('Please input how much you own of this coin : '))
req = ''
try:
    req = requests.get('https://api.nomics.com/v1/currencies/ticker?key=b24db6b794a971ab4caecfe738d3872a&ids='+coin+'&interval=1h,\
    30d&convert=USD&per-page=100&page=1')

    if req.status_code != 200:
        raise exceptions.RequestError
    if not req.json():
        raise exceptions.coinNotAvailable
    for x in req.json():
        coinPrice = float(x['price'])
except exceptions.RequestError:
    print("\nError has occured while raising the request")
    sys.exit(1)
except exceptions.coinNotAvailable:
    print("\nSorry! The coin you specified could not be found")
    sys.exit(1)
#we will be working on a new feature to have several coins here

totalAssets = coinAsset*coinPrice
today = date.today()
dat = today.strftime("%d/%m/%y")
print('\n\n##Crypto Prices' + '\n'+coin+' : ' + str(coinPrice) +
      '\n\n##Your Wallet \n'+coin+' : $'+str(totalAssets))
