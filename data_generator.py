from alice_blue import *
from time import sleep
import datetime
# import logging
import yfinance as yf
import json
import pandas as pd
import os


def connect_to_alice():
    global alice
    cwd = r"F:\Database\cred"
    cred = open(os.path.join(cwd, "cred.txt"), 'r')
    Lines = cred.readlines()

    username = Lines[0][:-1]
    password = Lines[1][:-1]
    twoFA = Lines[2][:-1]
    api_secret = Lines[3]

    access_token = AliceBlue.login_and_get_access_token(username=username, password=password, twoFA=twoFA,
                                                        api_secret=api_secret)
    alice = AliceBlue(username=username, password=password, access_token=access_token)
    print(alice.get_profile())
    return alice


def get_instruments():
    loc = r"F:\Database\Alice-data\symbol.xlsx"
    df1 = pd.read_excel(
        loc,
        engine='openpyxl',
        header=None
    )
    instrument_list = []
    for symbol in list(df1[0].values):
        instrument_list.append(alice.get_instrument_by_symbol('NSE', symbol))
    return list(df1[0].values), instrument_list


alice = connect_to_alice()
symbols, instrument_list = get_instruments()

socket_opened = False

filename = str(datetime.datetime.now().date()) + ".txt"

loc = os.path.join(r"F:\Database\Alice-data\data", filename)


def event_handler_quote_update(message):
    msg = {'exchange_time_stamp': message['exchange_time_stamp'],
           'instrument': message['instrument'].symbol,
           'expiry': message['instrument'].expiry,
           'ltp': message['ltp'],
           'volume': message['volume']}
    print(msg)
    # d.append(message)
    with open(loc, 'a') as redf:
        redf.write(str(msg) + "\n")


def open_callback():
    global socket_opened
    socket_opened = True


try:
    alice.start_websocket(subscribe_callback=event_handler_quote_update,
                          socket_open_callback=open_callback,
                          run_in_background=True)
    while not socket_opened:
        pass
    alice.subscribe(instrument_list, LiveFeedType.COMPACT)
    # sleep(7200)
except KeyboardInterrupt:
    print("Unsubscribe")
    alice.unsubscribe(instrument_list, LiveFeedType.COMPACT)
