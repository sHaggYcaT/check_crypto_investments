#!/usr/bin/env python3

import coinmarketcap
import time
import configparser
import sys, traceback

config = configparser.ConfigParser()

market = coinmarketcap.Market()
config.read('currency.ini')
investments_list = config.sections()


def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def currency_def(curr):
    cur_map = ConfigSectionMap(curr)
    if  ( ( 'amount' in cur_map )  and ( 'currency_bought' in cur_map) ) or ( curr == 'Bitcoin') and ( 'amount' in cur_map):
        if 'date' in cur_map:
            pass

        try:
            coin = market.ticker(curr)[0]
            #print (coin["name"],coin["price_usd"])
            print ("")
            #print(coin)
            print (coin["name"])
            if ('note' in cur_map ):
                print ("  ", "Note:",cur_map['note'])
            print ("  ",'We have',cur_map['amount'], coin['symbol'])
            coin_in_fiat_money = float(coin['price_usd']) * float(cur_map['amount'])
            print ("  ",'in USD it is =',coin_in_fiat_money)
            print ("  ",'Current market exhange rate is',coin['price_usd'],'USD')
            print ("  ",'price changed in 24h', coin["percent_change_24h"],'percents')
            print ("  ",'price changed in 7d', coin["percent_change_7d"], 'percents')
            if curr != 'Bitcoin':
                print ("  ", "We bought this coin or token using",cur_map['currency_bought'])
                currency_bought = cur_map['currency_bought']
                if currency_bought == 'USD':
                    print ("  ", "we bought it for ",cur_map['price_bought'], "USD")
                    delta = coin_in_fiat_money - float(cur_map['price_bought'])


                elif currency_bought == 'BTC':
                    btc_eq = market.ticker("Bitcoin")[0]
                    stay_btc = float(cur_map['price_bought']) * float(btc_eq['price_usd'])
                    delta = coin_in_fiat_money - stay_btc 
                    print ("  ", "we bought it for ",cur_map['price_bought'], "BTC. If we stay in BTC, then we have", stay_btc,'USD' )
                else:
                    print("There is an error in your INI file! Please fix.")


                print ('_________________________________________________')
                print ("  ", 'Our profit=',delta,'USD')
            else:
                delta = 0.0
            return { 'profit': delta, 'capital': coin_in_fiat_money }


        except:
            print ("exception!")
            print ("Exception in user code:")
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)

       



profit = 0.0
capital = 0.0

for curr in investments_list:
    returns = currency_def(curr)
    profit = profit + float(returns['profit'])
    capital = capital + returns['capital']


print ('=======================================================')
print ('Our total profit is',profit,'USD')
print ('And our total crypto capital is',capital,'USD')



