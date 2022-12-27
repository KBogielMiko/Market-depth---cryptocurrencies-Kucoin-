#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''Market depth - cryptocurrencies (KuCoin)'''


# In[ ]:


#Neccessary library for API commands


# In[ ]:


pip install kucoin-python  


# In[ ]:


from kucoin.market import market
import os
import pandas as pd
import numpy as np
api_key = 'key'
api_secret = 'secret'
api_passphrase = 'passphrase'


# In[ ]:


market = market.MarketData(key = api_key, secret = api_secret, passphrase = api_passphrase)


# In[ ]:


# first im gonna try to an operation with single coin


# In[ ]:


order_book = market.get_aggregated_orderv3('BTC-USDT')  # API documentation


# In[ ]:


order_book.keys()


# In[ ]:


type(order_book)


# In[ ]:


# 'asks' are neccessary for further operation


# In[ ]:


ask_btc = order_book['asks']


# In[ ]:


ask_btc[:5]


# In[ ]:


type(ask_btc)


# In[ ]:


type(ask_btc[0][1])


# In[ ]:


btc_df = pd.DataFrame(ask_btc, columns = ['price','amount'])  # df for adding column 'price'*'amount'


# In[ ]:


btc_df.head()


# In[ ]:


btc_df['price'] = btc_df['price'].astype(float)  # we need floats for multiple columns 'price'*'amount'
btc_df['amount'] = btc_df['amount'].astype(float) 


# In[ ]:


type(btc_df['price'][0])


# In[ ]:


type(btc_df['amount'][0])


# In[ ]:


btc_df['sum'] = btc_df['price']*btc_df['amount'] 


# In[ ]:


btc_df.drop('ask', axis = 'columns', inplace = True)


# In[ ]:


btc_df.head()


# In[ ]:


type(btc_df['sum'][0])


# In[ ]:


btc_list = btc_df.values.tolist() #change to list for faster calculations


# In[ ]:


btc_list[:5]


# In[ ]:


len(btc_list)


# In[ ]:


# I want to check, on which order through orderbook we are out of money - it means, that we gonna buy order after order till we spent whole 50K - with this way we gonna find a future price


# In[ ]:


actual_price_btc = btc_list[0][0]
cash = 2000000
result = []
for i in range(len(btc_list)):
    b = cash - btc_list[i][2]
    cash = b
    if cash <=0:
        result.append([actual_price_btc, btc_list[i][0], (btc_list[i][0]/actual_price_btc)/100])
        break


# In[ ]:


print(result)


# In[ ]:


####### Now we gonna do the same operation for rest coins 


# In[ ]:


from kucoin.client import Market


# In[ ]:


client = Market(url='https://api.kucoin.com')  # API documentation


# In[ ]:


tickers = client.get_all_tickers()  #we need all tickers for make a list with USDT tickers


# In[ ]:


tickers.keys()


# In[ ]:


tickers = pd.DataFrame(tickers['ticker'])


# In[ ]:


tickers.head()


# In[ ]:


tickers.set_index('symbol', inplace=True)


# In[ ]:


tickers.head()


# In[ ]:


list_tickers = list(tickers.index.values)


# In[ ]:


list_tickers[:5]


# In[ ]:


usdt_tickers = []
for i in list_tickers:
    if 'USDT' in i:
        usdt_tickers.append(i)    # only USDT tickers for further operations


# In[ ]:


usdt_tickers[:10]


# In[ ]:


len(usdt_tickers)


# In[ ]:


orderbook_usdt = []
for i in usdt_tickers:
    orderbook_usdt.append(market.get_aggregated_orderv3(i))


# In[ ]:


len(orderbook_usdt)


# In[ ]:


orderbook_usdt = orderbook_usdt[:-1]


# In[ ]:


len(orderbook_usdt)


# In[ ]:


orderbook_usdt[:1]


# In[ ]:


orderbook_usdt_asks = []
for i in orderbook_usdt:
       orderbook_usdt_asks.append(i['asks'])


# In[ ]:


# convert every single orderbook to seperated df


# In[ ]:


orderbook_usdt_df = []
for i in orderbook_usdt_asks:
    a = pd.DataFrame(i, columns = ['price','amount'])
    orderbook_usdt_df.append(a)


# In[ ]:


# whole strings to floats for 'sum' column


# In[ ]:


for i in orderbook_usdt_df:
    i['price'] = i['price'].astype(float)
    i['amount'] = i['amount'].astype(float)


# In[ ]:


type(orderbook_usdt_df[0]['price'][0])


# In[ ]:


#adding column 'sum' to every coins df


# In[ ]:


for i in orderbook_usdt_df:
    i['sum'] = i['price']*i['amount']


# In[ ]:


# moving back all to list  


# In[ ]:


orderbook_usdt_asks_list = []
for i in orderbook_usdt_df:
    a = i.values.tolist()
    orderbook_usdt_asks_list.append(a)


# In[ ]:


# what happen to every coin after putting 50k $ immadiatelely


# In[ ]:


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


# In[ ]:


final_list


# In[ ]:


usdt_tickers1 = usdt_tickers[:27]


# In[ ]:


len(usdt_tickers1)


# In[ ]:


final_df = pd.DataFrame(final_list, columns = ['first_price','final_price','% change'])


# In[ ]:


final_df['% change'] = final_df['% change']/100


# In[ ]:


final_df['Coin'] = [i for i in usdt_tickers1]


# In[ ]:


final_df.sort_values(by= '% change', ascending = False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




