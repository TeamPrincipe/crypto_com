# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 11:51:35 2021

@author: simosc

DA IMPLEMENTARE: 
    1) Json condizionali per endpoint: create_order, get_open_orders, get_order_history, get_open_orders, get_trades
    2) Gestione errore e RC
    
"""

from typing import Dict, Optional
import requests
import json
import hmac
import hashlib
import time
import datetime

class Client :
    
    API_URL = "https://api.crypto.{}/"
    PUBLIC_API_VERSION = 'v2'
    PRIVATE_API_VERSION = 'v2'    

    def __init__(
        self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Dict[str, str] = None, tld: str = 'com',
        testnet: bool = False
        ):
        
        self.tld = tld
        self.API_URL = self.API_URL.format(tld)
        self.API_KEY = api_key 
        self.API_SECRET = api_secret
        
    def signature(self,req,api_secret):
        """

        Parameters
        ----------
        req : dict
            Json with api request
        api_secret : str
            Secret API key

        Returns
        -------
        null : 
            Make digital sig for private rest api call. 

        """    
        # First ensure the params are alphabetically sorted by key
        paramString = ""
        
        if "params" in req:
          for key in sorted(req['params']):
            paramString += key
            paramString += str(req['params'][key])
        
        sigPayload = req['method'] + str(req['id']) + req['api_key'] + paramString + str(req['nonce'])
        
        req['sig'] = hmac.new(
          bytes(str(api_secret), 'utf-8'),
          msg=bytes(sigPayload, 'utf-8'),
          digestmod=hashlib.sha256
        ).hexdigest()

    # PUBLIC ENDPOINTS ------------------------------------------------------------------------------------------------------------------------------------------
    
    def get_instrument(self):
        """

        Parameters
        ----------


        Returns
        -------
        list : 
            exchange instruments. 

        """    
        
        # Request param
        req = {
          "id": 11,
          "method": "public/get-instruments",
          "nonce": int(time.time() * 1000)
        };        
        
        response = requests.get(self.API_URL + self.PUBLIC_API_VERSION + "/" + req["method"],
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["result"]["instruments"]
        
        return response
    
    def get_book(self, pair, depth):
        """

        Parameters
        ----------
        pair : str
            pair for which download the order book
        depth : int
            depth of the order book

        Returns
        -------
        dict : 
            Dict whit ask prices, bid prices, time. 

        """    
        
        # Request param
        req = {
          "method": "public/get-book",
        };        
        
        response = requests.get(self.API_URL + self.PUBLIC_API_VERSION + "/" + req["method"] + "?instrument_name=" + pair + "&depth=" + str(depth),
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["result"]["data"][0]
        
        return response
    
    def get_candlestick(self, pair, timeframe):
        """

        Parameters
        ----------
        pair : str
            pair for which download the hystorical data
        timeframe : str
            timeframe of data
            Available -> 1m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1D, 7D, 14D, 1M

        Returns
        -------
        list : 
            list od historical data. 

        """    
        
        # Request param
        req = {
          "method": "public/get-candlestick",
        };        
        
        response = requests.get(self.API_URL + self.PUBLIC_API_VERSION + "/" + req["method"] + "?instrument_name=" + pair + "&timeframe=" + timeframe,
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["result"]["data"]        
        
        return response   
    
    def get_ticker(self, all_pairs=True, pair : Optional[str] = None):
        """

        Parameters
        ----------
        all_pairs : bool
            default = True, make request for all available pairs
        pair : str
            optional, make request for single pair ("CRO_USDC")

        Returns
        -------
        dict : 
           dict with ask,bid,volume,price change data for pair\pairs

        """    
        
        # Request param
        req = {
          "method": "public/get-ticker",
        };       
        
        if all_pairs:
            response = requests.get(self.API_URL + self.PUBLIC_API_VERSION + "/" + req["method"],
                                     json=req,
                                     headers={"Content-Type":"application/json"})
        else:
            response = requests.get(self.API_URL + self.PUBLIC_API_VERSION + "/" + req["method"] + "?instrument_name=" + pair,
                                     json=req,
                                     headers={"Content-Type":"application/json"})
            
        response = json.loads(response.text)
        response = response["result"]["data"]        
        
        return response   
    
    def get_public_trades(self, all_pairs=True, pair : Optional[str] = None):
        """

        Parameters
        ----------
        all_pairs : bool
            default = True, make request for all available pairs
        pair : str
            optional, make request for single pair ("CRO_USDC")

        Returns
        -------
        list : 
           list of publi trades data for pair\pairs

        """    
        
        # Request param
        req = {
          "method": "public/get-trades",
        };       
        
        if all_pairs:
            response = requests.get(self.API_URL + self.PUBLIC_API_VERSION + "/" + req["method"],
                                     json=req,
                                     headers={"Content-Type":"application/json"})
        else:
            response = requests.get(self.API_URL + self.PUBLIC_API_VERSION + "/" + req["method"] + "?instrument_name=" + pair,
                                     json=req,
                                     headers={"Content-Type":"application/json"})
            
        response = json.loads(response.text)
        response = response["result"]["data"]        
        
        return response 
      
    # PRIVATE ENDPOINTS ------------------------------------------------------------------------------------------------------------------------------------------
    
    # SPOT TRADING API
    
    def get_account_summary(self, all_tickers=True, ticker : Optional[str] = None): 
        """

        Parameters
        ----------
        all_tickers : bool
            default = True, make request for all available tickers
        ticker : str
            optional, make request for single ticker ("CRO")

        Returns
        -------
        list : 
            account balances. 

        """   
        
        # Request param 
        if all_tickers:
            req = {
              "id": 11,
              "method": "private/get-account-summary",
              "api_key": self.API_KEY,
              "params": {},
              "nonce": int(time.time() * 1000)
            };
        else:
            req = {
              "id": 11,
              "method": "private/get-account-summary",
              "api_key": self.API_KEY,
              "params": {
                  "currency" : ticker
                  },
              "nonce": int(time.time() * 1000)
            };            
        
        # Signature for private call
        self.signature(req, self.API_SECRET)
        
        response = requests.post(self.API_URL + self.PRIVATE_API_VERSION + "/" + req["method"],
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["result"]["accounts"]
        
        return response
    
    def create_order(self, pair, side, Type, quantity,
                     price : Optional[float] = None,
                     notional : Optional[float] = None,
                     client_oid : Optional[str] = None,
                     time_in_force : Optional[str] = None,
                     exec_inst : Optional[str] = None,
                     trigger_price : Optional[float] = None): 
        """

        Parameters
        ----------
        pair : str
            e.g., ETH_CRO, BTC_USDT
        side : str
            BUY, SELL
        type : str
            LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT
        price : float
            Depends for LIMIT and STOP_LIMIT orders only: Unit price
        quantity : float
            Depends for LIMIT Orders, MARKET, STOP_LOSS, TAKE_PROFIT orders only: Order Quantity to be Sold
        notional : float
            Depends	For MARKET (BUY), STOP_LOSS (BUY), TAKE_PROFIT (BUY) orders only: amount to spend
        client_oid : str
            Optional Client order ID        
        time_in_force : str
            (Limit Orders Only) Options are: GOOD_TILL_CANCEL (Default if unspecified), FILL_OR_KILL, IMMEDIATE_OR_CANCEL
        exec_inst : str
            (Limit Orders Only) Options are: POST_ONLY, or leave empty
        trigger_price : float
            Used with STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders. Dictates when order will be triggered

        Returns
        -------
        list : 
           desc. 

        """   
        
        # Request param 
    
        # req = {
        #   "id": 11,
        #   "method": "private/create-order",
        #   "api_key": self.API_KEY,
        #   "params": {
        #       "instrument_name": pair,
        #       "side": side,
        #       "type": Type,
        #       "price": price,
        #       "quantity": quantity,
        #       "notional": notional,
        #       "client_oid": client_oid,
        #       "time_in_force": time_in_force,
        #       "exec_inst": exec_inst,
        #       "trigger_price": trigger_price
        #       },
        #   "nonce": int(time.time() * 1000)
        # };
        
        req = {
          "id": 11,
          "method": "private/create-order",
          "api_key": self.API_KEY,
          "params": {
              "instrument_name": pair,
              "side": side,
              "type": Type,
              "quantity": quantity
              },
          "nonce": int(time.time() * 1000)
        };
        
        # Signature for private call
        self.signature(req, self.API_SECRET)
        
        response = requests.post(self.API_URL + self.PRIVATE_API_VERSION + "/" + req["method"],
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["result"]
        
        print("Order created succesfully, order_id is:", response["order_id"])        
        
        return response
    
    def cancel_order(self, pair, order_id):
        """

        Parameters
        ----------
        pair : str
            e.g., ETH_CRO, BTC_USDT
        order_id : str
            order_id of the order

        Returns
        -------
        int : 
           RC = 0 order canceled succesfully 

        """   
        
        # Request param 
        req = {
          "id": 11,
          "method": "private/cancel-order",
          "api_key": self.API_KEY,
          "params": {
              "instrument_name": pair,
              "order_id": order_id,
              },
          "nonce": int(time.time() * 1000)
        };      

        # Signature for private call
        self.signature(req, self.API_SECRET)
        
        response = requests.post(self.API_URL + self.PRIVATE_API_VERSION + "/" + req["method"],
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["code"]
        
        if response == 0:
            print("Order canceled succesfully, order_id is:", order_id)
        else: 
            print("Error, order not canceled, order_id is:", order_id)
            
        return response
    
    def cancel_all_orders(self, pair):
        """

        Parameters
        ----------
        pair : str
            e.g., ETH_CRO, BTC_USDT

        Returns
        -------
        int : 
           RC = 0 order canceled succesfully 

        """   
        
        # Request param 
        req = {
          "id": 11,
          "method": "private/cancel-all-orders",
          "api_key": self.API_KEY,
          "params": {
              "instrument_name": pair,
              },
          "nonce": int(time.time() * 1000)
        };      

        # Signature for private call
        self.signature(req, self.API_SECRET)
        
        response = requests.post(self.API_URL + self.PRIVATE_API_VERSION + "/" + req["method"],
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["code"]
        
        if response == 0:
            print("All Orders for pair:", pair, "canceled succesfully")
        else: 
            print("Error, orders for pair:", pair, "not canceled")
            
        return response
    
    def get_order_history(self, all_pairs=True, 
                          pair : Optional[str] = None,
                          start_ts : Optional[int] = int(datetime.datetime.timestamp(datetime.datetime.now() - datetime.timedelta(days=1)) * 1000),
                          end_ts : Optional[int] = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000),
                          page_size : Optional[int] = None,
                          page : Optional[int] = None):
        """

        Parameters
        ----------
        all_pairs : bool
            default = True, make request for all available pairs
        pair : str
            optional, make request for single pair ("CRO_USDC")
        start_ts : timestamp
            Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago
        end_ts : timestamp
            End timestamp (milliseconds since the Unix epoch) - defaults to 'now'
        page_size : int 
            Page size (Default: 20, max: 200)
        page : int
            Page number (0-based)

        Returns
        -------
        list : 
           desc. 

        """
        
        # Request param 
        if all_pairs:
            req = {
              "id": 11,
              "method": "private/get-order-history",
              "api_key": self.API_KEY,
              "params": {
                  "start_ts" : start_ts,
                  "end_ts" : end_ts,
                  #"page_size" : page_size,
                  #"page" : page                  
                  },
              "nonce": int(time.time() * 1000)
            };
        else:
            req = {
              "id": 11,
              "method": "private/get-order-history",
              "api_key": self.API_KEY,
              "params": {
                  "instrument_name" : pair,
                  "start_ts" : start_ts,
                  "end_ts" : end_ts,
                  #"page_size" : page_size,
                  #"page" : page    
                  },
              "nonce": int(time.time() * 1000)
            };  

        # Signature for private call
        self.signature(req, self.API_SECRET)
        
        response = requests.post(self.API_URL + self.PRIVATE_API_VERSION + "/" + req["method"],
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["result"]["order_list"]
        
        return response
    
    def get_open_orders(self, all_pairs=True, 
                       pair : Optional[str] = None, 
                       page_size : Optional[int] = None,
                       page : Optional[int] = None):
        """

        Parameters
        ----------
        all_pairs : bool
            default = True, make request for all available pairs
        pair : str
            optional, make request for single pair ("CRO_USDC")
        page_size : int 
            Page size (Default: 20, max: 200)
        page : int
            Page number (0-based)

        Returns
        -------
        list : 
           desc. 

        """          

        # Request param 
        if all_pairs:
            req = {
              "id": 11,
              "method": "private/get-open-orders",
              "api_key": self.API_KEY,
              "params": {
                  #"page_size" : page_size,
                  #"page" : page                  
                  },
              "nonce": int(time.time() * 1000)
            };
        else:
            req = {
              "id": 11,
              "method": "private/get-open-orders",
              "api_key": self.API_KEY,
              "params": {
                  "instrument_name" : pair,
                  #"page_size" : page_size,
                  #"page" : page    
                  },
              "nonce": int(time.time() * 1000)
            };  
        
        # Signature for private call
        self.signature(req, self.API_SECRET)
        
        response = requests.post(self.API_URL + self.PRIVATE_API_VERSION + "/" + req["method"],
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["result"]["order_list"]
        
        return response

    def get_order_detail(self, order_id):
        """

        Parameters
        ----------
        order_id : str
            order_id of the order

        Returns
        -------
        dict : 
           desc

        """           

        # Request param 
        req = {
          "id": 11,
          "method": "private/get-order-detail",
          "api_key": self.API_KEY,
          "params": {
              "order_id": order_id,
              },
          "nonce": int(time.time() * 1000)
        };      

        # Signature for private call
        self.signature(req, self.API_SECRET)
        
        response = requests.post(self.API_URL + self.PRIVATE_API_VERSION + "/" + req["method"],
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)    
        response = response["result"]
        
        return response 
    
    def get_trades(self, all_pairs=True, 
                          pair : Optional[str] = None,
                          start_ts : Optional[int] = int(datetime.datetime.timestamp(datetime.datetime.now() - datetime.timedelta(days=1)) * 1000),
                          end_ts : Optional[int] = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000),
                          page_size : Optional[int] = None,
                          page : Optional[int] = None):
        """

        Parameters
        ----------
        all_pairs : bool
            default = True, make request for all available pairs
        pair : str
            optional, make request for single pair ("CRO_USDC")
        start_ts : timestamp
            Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago
        end_ts : timestamp
            End timestamp (milliseconds since the Unix epoch) - defaults to 'now'
        page_size : int 
            Page size (Default: 20, max: 200)
        page : int
            Page number (0-based)

        Returns
        -------
        list : 
           A trade list for which the maximum duration between start_ts and end_ts is 24 hours.
           For users looking to pull longer historical trade data, users can create a loop to make a request for each 24-period from the desired start to end time. 

        """
        
        # Request param 
        if all_pairs:
            req = {
              "id": 11,
              "method": "private/get-trades",
              "api_key": self.API_KEY,
              "params": {
                  "start_ts" : start_ts,
                  "end_ts" : end_ts,
                  #"page_size" : page_size,
                  #"page" : page                  
                  },
              "nonce": int(time.time() * 1000)
            };
        else:
            req = {
              "id": 11,
              "method": "private/get-trades",
              "api_key": self.API_KEY,
              "params": {
                  "instrument_name" : pair,
                  "start_ts" : start_ts,
                  "end_ts" : end_ts,
                  #"page_size" : page_size,
                  #"page" : page    
                  },
              "nonce": int(time.time() * 1000)
            };  

        # Signature for private call
        self.signature(req, self.API_SECRET)
        
        response = requests.post(self.API_URL + self.PRIVATE_API_VERSION + "/" + req["method"],
                                 json=req,
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        response = response["result"]["trade_list"]
        
        return response

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    