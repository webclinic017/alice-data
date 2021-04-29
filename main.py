from alice_blue import *
from time import sleep
import datetime
# import logging
import yfinance as yf
import json
import os

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
