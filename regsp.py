import re, requests, string
import logging
import requests
import time
import string
import random
import asyncio
import re
import base64
import json
import sys
import urllib3
import http.client
import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

SK = os.getenv('SK')
session = requests.session()
letters = string.ascii_lowercase

PWD = ''.join(random.choice(letters) for i in range(10))
UA = 'Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'
time1 = time.time()
def regsp(input):
  
  First = ''.join(random.choice(letters) for i in range(6))
  Last = ''.join(random.choice(letters) for i in range(6))

  Name = f'{First}+{Last}'
  Email = f'cheap{First}.{Last}@cheapluxury.com'
  pass1 = "cocainitne"
  load4 = {
   "birth_day": '01',
   "birth_month": '01',
  "birth_year": '2002',
"collect_personal_info": 'undefined',
"creation_flow": '',
"creation_point": 'https://www.spotify.com/uk/',
"displayname": 'spoti',
"email": Email ,
"gender": 'male',
"iagree": '1',
"key": 'a1e486e2729f46d6bb368d6b2bcda326',
"password": pass1,
"password_repeat": pass1,
"platform": 'www',
"referrer": '',
"send-email": '1',
"thirdpartyemail": '0',
"fb": '0'
   }


  header = {
            "accept": "*/*",
            "content-type": "application/json",
            "host": 'spclient.wg.spotify.com',
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"

        }
    
    
 # proxies = {
    #'http': 'http://whmtsthekl:8i0Kc3nKw7@108.165.230.30:3486/',
    #'https': 'http://whmtsthekl:8i0Kc3nKw7@108.165.230.30:3486/'}
    
  r = requests.post(
  f'https://spclient.wg.spotify.com/signup/public/v1/account', data=load4, headers=header).json()
    
  print(r)
    
  if 'username' in r:
            ct = r['country']
            return (f'''
✅𝙎𝙞𝙜𝙣 𝙪𝙥 𝙤𝙣 𝙨𝙥𝙤𝙩𝙞𝙛𝙮 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮
<b>Email:</b><code>{Email}</code>
<b>Pass:</b><code>{pass1}</code>
<b>Country: {ct}</b>
''')

  if 'errors' in r:
            msg = r['errors']
            
            return (f'''
{msg}
''')  