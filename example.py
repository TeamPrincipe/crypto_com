# -*- coding: utf-8 -*-
"""

@author: simosc
"""

from crypto_com.client import Client

API_KEY = <YOUR_API_KEY>
API_SECRET = <YOUR_API_SECRET>

# Initialize Client 
test = Client(API_KEY,API_SECRET)

# PUBLIC 
# get_instruments 
inst = test.get_instrument()

# get_book
book = test.get_book("BTC_USDC", 10)

# get_candlestick 
hist = test.get_candlestick("BTC_USDC", "1D")

# get_ticker
last_data = test.get_ticker()
last_data_single = test.get_ticker(all_pairs=False, pair="CRO_USDC")

# get_public_trades 
last_trades = test.get_public_trades()
last_trades_single = test.get_public_trades(all_pairs=False, pair="CRO_USDC")

# PRIVATE
# Account summary
account_summary_single = test.get_account_summary(all_tickers=False, ticker="CRO")
account_summary = test.get_account_summary()

# create_order
#order_test = test.create_order("CRO_USDC", "BUY", "MARKET", 1)

# cancel_order
cancel_order = test.cancel_order("CRO_USDT", "2066499456690669985")

# cancel_all_orders
cancel_all = test.cancel_all_orders("CRO_USDT")

# get_open_orders
open_orders = test.get_open_orders()
open_orders_single = test.get_open_orders(all_pairs=False, pair="CRO_USDT")

# get_order_history
order_hist = test.get_order_history()
order_hist_single = test.get_order_history(all_pairs=False, pair="CRO_USDC")

# get_order_detail
order_detail = test.get_order_detail("2063978173632069989")

# get_trades 
trades = test.get_trades()
trades_single = test.get_trades(all_pairs=False, pair="CRO_USDC")





