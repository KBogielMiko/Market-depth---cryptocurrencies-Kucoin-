'''Market depth - cryptocurrencies (KuCoin)'''

#Neccessary library for API commands

pip install kucoin-python  

#Library import

from kucoin.market import market
import os
import pandas as pd
import numpy as np
api_key = 'key'
api_secret = 'secret'
api_passphrase = 'passphrase'


market = market.MarketData(key = api_key, secret = api_secret, passphrase = api_passphrase)   # API


# At the begining im gonna try to do it with a single coin


order_book = market.get_aggregated_orderv3('BTC-USDT')  # API documentation
order_book.keys()

type(order_book)

# 'asks' are neccessary for further operation
ask_btc = order_book['asks']

ask_btc[:5]
type(ask_btc)
type(ask_btc[0][1])


# df for implement column 'price'*'amount'
btc_df = pd.DataFrame(ask_btc, columns = ['price','amount'])
btc_df.head()

# we need floats for multiple columns 'price'*'amount'
btc_df['price'] = btc_df['price'].astype(float) 
btc_df['amount'] = btc_df['amount'].astype(float) 
type(btc_df['price'][0])
type(btc_df['amount'][0])

# new column
btc_df['sum'] = btc_df['price']*btc_df['amount'] 
btc_df.head()
type(btc_df['sum'][0])

#change to list for faster calculations
btc_list = btc_df.values.tolist() 

btc_list[:5]
len(btc_list)

''' I want to check, on which order through orderbook we are out of money - 
it means, that we gonna pass order after order till we spent whole 50K - with this way we gonna find a future price'''

actual_price_btc = btc_list[0][0]
cash = 2000000
result = []
for i in range(len(btc_list)):
    b = cash - btc_list[i][2]
    cash = b
    if cash <=0:
        result.append([actual_price_btc, btc_list[i][0], (btc_list[i][0]/actual_price_btc)/100])
        break
        
print(result)

####### Now I'm gonna do the same operation for rest coins 

from kucoin.client import Market

client = Market(url='https://api.kucoin.com')  # API documentation

#all tickers for make a list with USDT tickers

tickers = client.get_all_tickers()  #API doccumentation
tickers.keys()
tickers = pd.DataFrame(tickers['ticker'])
tickers.head()

tickers.set_index('symbol', inplace=True)
tickers.head()

list_tickers = list(tickers.index.values)
list_tickers[:5]

# only USDT tickers for further operations

usdt_tickers = []
for i in list_tickers:
    if 'USDT' in i:
        usdt_tickers.append(i)    

usdt_tickers[:10]
len(usdt_tickers)


# getting data of all USDT tickers
orderbook_usdt = []
for i in usdt_tickers:
    orderbook_usdt.append(market.get_aggregated_orderv3(i))

len(orderbook_usdt)
orderbook_usdt = orderbook_usdt[:-1]
len(orderbook_usdt)
orderbook_usdt[:1]

# only asks - we are not interested in bids 

orderbook_usdt_asks = []
for i in orderbook_usdt:
       orderbook_usdt_asks.append(i['asks'])

# convert every single orderbook to seperated df

orderbook_usdt_df = []
for i in orderbook_usdt_asks:
    a = pd.DataFrame(i, columns = ['price','amount'])
    orderbook_usdt_df.append(a)

# whole strings to floats for create 'sum' column

for i in orderbook_usdt_df:
    i['price'] = i['price'].astype(float)
    i['amount'] = i['amount'].astype(float)

type(orderbook_usdt_df[0]['price'][0])

#adding column 'sum' to every coins df

for i in orderbook_usdt_df:
    i['sum'] = i['price']*i['amount']

# moving back all to list  

orderbook_usdt_asks_list = []
for i in orderbook_usdt_df:
    a = i.values.tolist()
    orderbook_usdt_asks_list.append(a)

    
# what happen to every coin after putting 50k $ immadiatelely

final_list = []
for i in orderbook_usdt_asks_list:
    cash = 50000
    actual_price = i[0][0]
    for j in i:
        b = cash - j[2]
        cash = b
        if cash <=0:
            final_list.append([actual_price,j[0],(j[0]/actual_price)*100])
            break

print(final_list)

usdt_tickers1 = usdt_tickers[:27]
len(usdt_tickers1)
final_df = pd.DataFrame(final_list, columns = ['first_price','final_price','% change'])
final_df['% change'] = final_df['% change']/100
final_df['Coin'] = [i for i in usdt_tickers1]
final_df.sort_values(by= '% change', ascending = False)
