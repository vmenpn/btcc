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


def getcc_check(input):
  input = re.sub('[a-zA-Z]', '', str(input))
  # list = input.replace('/','').split('\n')
  input = input.replace('/','|')
  list = re.findall(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
  
  # print(x)
  print(list)
  if list == "":
    return f"""<b>➡️SCRAPE CC
----------------------------------------------
Status: CC Not Found!!❌
----------------------------------------------</b>
  """
  start=time.time()
  result = ""
  for i in range(len(list)):
   if len(list[i]) not in [26,28]:
     pass
   else:
    card = list[i]
    ok = f'''<code>{card}</code>\n'''
    result += ok
  end=time.time()
  tm=f'{round((end-start),2)}s'
  print(result)
  return f"""<b>➡️SCRAPE CC
----------------------------------------------
Status: Success!!! ✅
Get: {len(list)} CCs
----------------------------------------------
{result}
----------------------------------------------</b>"""






