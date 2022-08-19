import logging
import os
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
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from telegram.ext.dispatcher import run_async

from cv import check_cv
from ck import check_ck
from sk import check_sk
from cc import check_cc
from vbv import check_vbv
from mk2 import check_mk2
from csk import check_csk
from regsp import regsp
from c import check_c
from tkfb import tkfb
from massc import single_check, mass_check
from massv import single_check, massv_check
from getcc import getcc_check
from getfshare import getfs

#import Response as R
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

admin = {
  '1924942921',
  '1659977716'
}
f = open("listuserban.txt", "r")
listban = f.read().split("\n")
f1 = open("user.txt", "r")
listuser = f1.read().split("\n")
f2 = open("listchat.txt", "r")
listchat = f2.read().split("\n")

def acp_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if not f'{ID}' in admin:
   update.message.reply_text(f'<b>Không được phép xài lệnh này</b>',parse_mode = "html")
   
 if f'{ID}' in admin:
   if f'{chatid}' in listchat:
      return update.message.reply_text(f'<b> Chat <code>{chatid}</code> đã được cấp quyền rồi</b>',parse_mode = "html")
   
   else:
    f2 = open("listchat.txt", "a")
    f2.write(f'{chatid}\n')
    update.message.reply_text(f'<b> Cấp quyền cho chat <code>{chatid}</code> thành công</b>',parse_mode = "html")



def register_command(update: Update, context: CallbackContext) -> None:
  ID = update.effective_user.id
  username = update.effective_user.username
  First = update.effective_user.first_name 
  f1 = open("user.txt", "r")
  listuser = f1.read().split("\n")
  chatid= update.message.chat.id 
  f2 = open("listchat.txt", "r")
  listchat = f2.read().split("\n")
  if f'{chatid}' in listchat:
    if f'{ID}' in listuser:
      return update.message.reply_text(f'<b> User <code>{ID}</code> đã đăng ký rồi</b>',parse_mode = "html")
    else:  
     f1 = open("user.txt", "a")
     f1.write(f'{ID}\n')
     update.message.reply_text(f'<b> Đã đăng kí thành công <a href="tg://user?id={ID}">{First}</a>\nID : <code>{ID}</code></b>',parse_mode = "html")
  else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")
    

def chan_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 if not f'{ID}' in admin:
   update.message.reply_text(f'<b>Không được phép xài lệnh này</b>',parse_mode = "html")
   
 if f'{ID}' in admin:
   id = update.message.reply_to_message.from_user.id
   username = update.message.reply_to_message.from_user.username
   First = update.message.reply_to_message.from_user.first_name
   if id == ID:
     update.message.reply_text(f'<b> Chủ đó</b>',parse_mode = "html")
   else:
    f = open("listuserban.txt", "a")
    f.write(f'{id}\n')
    update.message.reply_text(f'<b> Đã cấm người dùng <a href="tg://user?id={id}">{First}</a>\nID : <code>{id}</code></b>',parse_mode = "html")
  
  
    
def unchanall_command(update: Update, context: CallbackContext) -> None:
  ID = update.effective_user.id
  if not f'{ID}' in admin:
   update.message.reply_text(f'<b>Không được phép xài lệnh này</b>',parse_mode = "html")
  if f'{ID}' in admin:
   
   f = open("listuserban.txt", "r+")
   f.truncate(0)
   f.close()
   update.message.reply_text(f'<b> Đã bỏ cấm tất cả người dùng </b>',parse_mode = "html")
  


def unchan_command(update: Update, context: CallbackContext) -> None:
  ID = update.effective_user.id
  f1 = open("user.txt", "r")
  listuser = f1.read().split("\n")
  if not f'{ID}' in admin:
   update.message.reply_text(f'<b>Không được phép xài lệnh này</b>',parse_mode = "html")
  if f'{ID}' in admin:
   id = update.message.reply_to_message.from_user.id
   if id == ID:
     update.message.reply_text(f'<b> Chủ đó</b>',parse_mode = "html")
   else:
    id = update.message.reply_to_message.from_user.id
    username = update.message.reply_to_message.from_user.username
    First = update.message.reply_to_message.from_user.first_name
    f = open("listuserban.txt", "r")
    text = f.read()
    f = open("listuserban.txt", "w")
    un = text.replace(f'{id}', '')
    f.write(un)
    update.message.reply_text(f'<b> Đã bỏ cấm người dùng <a href="tg://user?id={id}">{First}</a>\nID : <code>{id}</code></b>',parse_mode = "html")
  
 

print("Bot Starting....")
def start_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:  
    update.message.reply_text(f'Hello @{update.effective_user.username}\nCmds \n/csk Charge 0.8$ 3rq\n/ck Charge 0.8$ 2rq \n/cv 4.99$\n/vbv check vbv\n/mk2 site 2ds\n/cc check auth\n/sk CHeck sk\n/regsp REG Spotify\n/tkfb user:pass (lấy token facebook)',parse_mode = "html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
  update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")   

    
def bin_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat: 
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:  
     is_bot = update.effective_user.is_bot
     username = update.effective_user.username
     first = update.effective_user.first_name
    
     BIN = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     BIN = BIN.strip('/bin')
     print(BIN)
     if len(BIN) < 6:
         return (
                   'Send bin not ass'
        )
     r = requests.get(f'http://binchk-api.vercel.app/bin={BIN}').json()
     
     print(r)
    
    
   
     update.message.reply_text(f'''
BIN⇢ <code>{BIN}</code>
Brand⇢ <b>{r["brand"]}</b>
Type⇢ <b>{r["type"]}</b>
Level⇢ <b>{r["level"]}</b>
Bank⇢ <b>{r["bank"]}</b>
Phone⇢ <b>{r["phone"]}</b>
Currency⇢ <b>{r["currency"]}</b>
Country⇢ <b>{r["country"]}({r["code"]})[{r["flag"]}]</b>
SENDER: <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar
''',parse_mode = "html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html") 
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")   
def info(update: Update, context: CallbackContext) -> None: 
        
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
         is_bot = update.effective_user.is_bot
         username = update.effective_user.username
         first = update.effective_user.first_name
         chatid= update.message.chat.id 
         print("check by "+first)
         update.message.reply_text(f'''
═════════╕
<b>USER INFO</b>
<b>USER ID:</b> <code>{ID}</code>
<b>USERNAME:</b> @{username}
<b>FIRSTNAME:</b> {first}
<b>BOT:</b> {is_bot}
<b>CHAT ID:</b> <code>{chatid}</code>
╘═════════''',parse_mode = "html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")    
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")



def ck_command(update: Update, context: CallbackContext) -> None:
  
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    is_bot = update.effective_user.is_bot
    username = update.effective_user.username
    first = update.effective_user.first_name
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
     msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
     card = x.group(0)
     input = input.strip('/v')
     msg = update.message.reply_text(f'<b>Checking... Please Wait...</b>\n<b>CC:</b><code>{card}</code>', parse_mode="html")
     res_cc = check_ck(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")    
  
def cv_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat: 
  if f'{ID}' in listuser:  
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    username = update.message.from_user.username
    ID = update.message.from_user.id
    first = update.effective_user.first_name
    print(username)
  
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
     msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
     card = x.group(0)
     input = input.strip('/cv')
     msg = update.message.reply_text(f'<b>Checking... Please Wait...</b>\n<b>CC:</b><code>{card}</code>', parse_mode="html")
  #print(input)
     res_cc = check_cv(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html") 
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")   
  
def sk_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:  
  if f'{ID}' in listuser:  
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    ID = update.effective_user.id
    is_bot = update.effective_user.is_bot
    username = update.effective_user.username
    first = update.effective_user.first_name
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
     msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
    
     msg = update.message.reply_text(f'<b>Checking... Please Wait...</b>\n<b>CC:</b><code>{input}</code>', parse_mode="html")
  #print(input)
     res_cc = check_sk(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")    

def cc_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser:  
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    ID = update.effective_user.id
    is_bot = update.effective_user.is_bot
    username = update.effective_user.username
    first = update.effective_user.first_name
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
     msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     input = input.strip('/cc')
     x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
     card = x.group(0)
     msg = update.message.reply_text(f'<b>Checking... Please Wait...</b>\n<b>CC:</b><code>{card}</code>', parse_mode="html")
     res_cc = check_cc(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")   

def vbv_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    ID = update.effective_user.id
    is_bot = update.effective_user.is_bot
    username = update.effective_user.username
    first = update.effective_user.first_name
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
     msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     input = input.strip('/vbv')
     x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
     card = x.group(0)
     msg = update.message.reply_text(f'<b>Checking... Please Wait...</b>\n<b>CC:</b><code>{card}</code>', parse_mode="html")
     res_cc = check_vbv(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")   

def mk2_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    ID = update.effective_user.id
    is_bot = update.effective_user.is_bot
    username = update.effective_user.username
    first = update.effective_user.first_name
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
     msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     input = input.strip('/mk2')
     x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
     card = x.group(0)
     msg = update.message.reply_text(f'<b>Checking... Please Wait...</b>\n<b>CC:</b><code>{card}</code>', parse_mode="html")
     res_cc = check_mk2(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")

def csk_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    ID = update.effective_user.id
    is_bot = update.effective_user.is_bot
    username = update.effective_user.username
    first = update.effective_user.first_name
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
     msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     input = input.strip('/csk')
     x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
     card = x.group(0)
     msg = update.message.reply_text(f'<b>Checking... Please Wait...</b>\n<b>CC:</b><code>{card}</code>', parse_mode="html")
     res_cc = check_csk(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html") 
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")   
    
def regsp_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    msg = update.message.reply_text(f'<b> Please Wait...</b>', parse_mode="html")
    ID = update.effective_user.id
    is_bot = update.effective_user.is_bot
    username = update.effective_user.username
    first = update.effective_user.first_name
    print(username)
    input = update.message.text 
    res_cc = regsp(input)
    msg.edit_text(f'''{res_cc}\n<b>Request</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")  
  
def c_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat: 
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    ID = update.effective_user.id
    is_bot = update.effective_user.is_bot
    username = update.effective_user.username
    first = update.effective_user.first_name
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
     msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     input = input.strip('/csk')
     x = re.search(r"(?:3|4|5|6)\d{14,15}\|\d{2}\|\d{2,4}\|\d{3,4}", input)
     card = x.group(0)
     msg = update.message.reply_text(f'<b>Checking... Please Wait...</b>\n<b>CC:</b><code>{card}</code>', parse_mode="html")
     res_cc = check_c(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")   

def tkfb_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 if f'{ID}' in listuser: 
  if f'{ID}' in listban:
   return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
  else:
   ID = update.effective_user.id
   is_bot = update.effective_user.is_bot
   username = update.effective_user.username
   first = update.effective_user.first_name
   print(username)
   if len(context.args) == 0 and update.message.reply_to_message == None:
    msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
    msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
   else:
    input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
    input = input.strip('/tkfb ')
    msg = update.message.reply_text(f'<b>Checking... Please Wait...</b>', parse_mode="html")
    res_cc = tkfb(input)
    msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
 if not f'{ID}' in listuser:
  return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")

def mass_chargesk_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id 
 is_bot = update.effective_user.is_bot
 username = update.effective_user.username
 first = update.effective_user.first_name
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    msg = update.message.reply_text("<b>Checking...</b>", parse_mode="html")
    username = update.message.from_user.username
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg.edit_text("<b>❌DATA NOT FOUND❌", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     input = input.strip('/mc')
     res_cc = mass_check(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")   
################################################
    
def massv_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id 
 is_bot = update.effective_user.is_bot
 username = update.effective_user.username
 first = update.effective_user.first_name
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    msg = update.message.reply_text("<b>Checking...</b>", parse_mode="html")
    username = update.message.from_user.username
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg.edit_text("<b>❌DATA NOT FOUND❌", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     input = input.strip('/mv')
     res_cc = massv_check(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")
################################################

def getcc_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id 
 is_bot = update.effective_user.is_bot
 username = update.effective_user.username
 first = update.effective_user.first_name
 f1 = open("user.txt", "r")
 listuser = f1.read().split("\n")
 chatid= update.message.chat.id 
 f2 = open("listchat.txt", "r")
 listchat = f2.read().split("\n")
 if f'{chatid}' in listchat:
  if f'{ID}' in listuser: 
   if f'{ID}' in listban:
    return update.message.reply_text(f'<b>Bạn đã bị cấm sử dụng bot</b>', parse_mode="html")
   else:
    msg = update.message.reply_text("<b>Checking...</b>", parse_mode="html")
    username = update.message.from_user.username
    print(username)
    if len(context.args) == 0 and update.message.reply_to_message == None:
     msg.edit_text("<b>❌DATA NOT FOUND❌", parse_mode = "html")
    else:
     input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
     input = input.strip('/getcc')
     res_cc = getcc_check(input)
     msg.edit_text(f'''{res_cc}\n<b>CHECK BY</b>➟ <a href="tg://user?id={ID}">{first}</a>\n<b>Bot by:</b> @kambalkavar''', parse_mode="html")
  if not f'{ID}' in listuser:
   return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")
 else:
    update.message.reply_text(f'<b> Không xài được đâu</b>',parse_mode = "html")   
################################################

def getfs_command(update: Update, context: CallbackContext) -> None:
 ID = update.effective_user.id
 if not f'{ID}' in admin:
   update.message.reply_text(f'<b>Không được phép xài lệnh này</b>',parse_mode = "html")
 if f'{ID}' in admin:
   ID = update.effective_user.id
   is_bot = update.effective_user.is_bot
   username = update.effective_user.username
   first = update.effective_user.first_name
   print(username)
   if len(context.args) == 0 and update.message.reply_to_message == None:
    msg = update.message.reply_text(f'<b>Please Wait...</b>', parse_mode="html")
    msg.edit_text("<b>❌DATA NOT FOUND❌\n</b>", parse_mode = "html")
   else:
    input = update.message.text if len(context.args) != 0 else update.message.reply_to_message.text
    input = input.strip('/getfs ')
    msg = update.message.reply_text(f'<b>Please Wait...</b>\n<b>Link: </b><code>{input}</code>', parse_mode="html")
    res_cc = getfs(input)
    msg.edit_text(f'''<code>/mirror https://{res_cc}</code>''', parse_mode="html")
 if not f'{ID}' in listuser:
  return update.message.reply_text(f'<b>Bạn chưa đăng ký\nHãy dùng /register</b>', parse_mode="html")  

def main():
  updater = Updater(os.getenv("TOKEN"))
  dp = updater.dispatcher
  
  # Define các lệnh mà mọi người cần
  # Param thứ nhất là nội dung câu lệnh, param thứ 2 là hàm để chạy lệnh đó
  dp.add_handler(CommandHandler('start', start_command))
  dp.add_handler(CommandHandler('info', info))
  dp.add_handler(CommandHandler('id', info))
  dp.add_handler(CommandHandler('cv', cv_command))
  dp.add_handler(CommandHandler('v', ck_command))
  dp.add_handler(CommandHandler('sk', sk_command))
  dp.add_handler(CommandHandler('cc', cc_command))
  dp.add_handler(CommandHandler('vbv', vbv_command))
  dp.add_handler(CommandHandler('mk2', mk2_command))
  dp.add_handler(CommandHandler('ck', csk_command))
  dp.add_handler(CommandHandler('regsp', regsp_command))
  dp.add_handler(CommandHandler('bin', bin_command))
  dp.add_handler(CommandHandler('csk', c_command))
  dp.add_handler(CommandHandler('tkfb', tkfb_command))
  dp.add_handler(CommandHandler('mc', mass_chargesk_command))
  dp.add_handler(CommandHandler('mv', massv_command))
  dp.add_handler(CommandHandler('chan', chan_command))
  dp.add_handler(CommandHandler('unchanall', unchanall_command))
  dp.add_handler(CommandHandler('unchan', unchan_command))
  dp.add_handler(CommandHandler('register', register_command))
  dp.add_handler(CommandHandler('getcc', getcc_command))
  dp.add_handler(CommandHandler('getfs', getfs_command))
  dp.add_handler(CommandHandler('acp', acp_command))
  
  #dp.add_handler(MessageHandler(Filters.text, handle_message))
  updater.start_polling()
  updater.idle()

main()