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
import ssl
from parsel import Selector
from bs4 import BeautifulSoup
import lxml.html as html

fsmail = os.getenv('fsmail')
fspass = os.getenv('fspass')

session = requests.session()
letters = string.ascii_lowercase
first = ''.join(random.choice(letters) for i in range(6))
last = ''.join(random.choice(letters) for i in range(6))
PWD = ''.join(random.choice(letters) for i in range(10))
name = f'{first}+{last}'
email = f'{first}.{last}@gmail.com'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
def getfs(input):
  load = {
    "user_email": fsmail,
    "password": fspass,
    "app_key": "dMnqMMZMUnN5YpvKENaEhdQQ5jxDqddt"
  }
  

  header = {
      
      "content-type": "application/json",
      #"Fshare-User-Agent": "vmenpn-R81X9Q",
     "User-Agent": "vmenpn-R81X9Q",
       "Pragma": "no-cache",
      "Accept": "*/*"
  }
    
      

  r1 = session.post('https://api.fshare.vn/api/user/login',
                    json=load, headers=header)
  res1 = r1.json()
  msg = res1['msg']
  print(msg)
  if 'Login successfully!' in r1.text:
    token = res1['token']
    session_id = res1['session_id']
    load1 = {
      "url": input,
      "password": "",
      "token": token,
      "zipflag": "0"
    }
    header1 = {
      
      "content-type": "application/json",
      "Fshare-User-Agent": "vmenpn-R81X9Q",
     #"User-Agent": "vmenpn-R81X9Q",
       "Pragma": "no-cache",
      "Accept": "*/*",
      "Cookie": "session_id="+session_id
  }
    r2 = session.post('https://api.fshare.vn/api/session/download',
                    json=load1, headers=header1)
    res2 = r2.json()
    print(res2)
    link = res2['location']
    r3 = session.get('https://api.fshare.vn/api/user/logout', headers=header1)
    r3 = r3.json()
    print(r3)
    load = {
      "u":link
    }
    header = {
            "user-agent": UA,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "accept-Language": "en-GB,en;q=0.9,en-US;q=0.8"

    }
    r4 = session.post('https://www.shorturl.at/shortener.php',
                          data=load, headers=header)
    soup = BeautifulSoup(r4.text, 'html.parser')
    tk = soup.find("input", {"id": "shortenurl"})
    
    print(tk)
    link1 = tk.get('value')
    print(link1)
    
    return (f'''{link1}''')
  else:
    return (f'''<b>Get link Fail</b>
''')