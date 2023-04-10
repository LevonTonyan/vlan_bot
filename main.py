import telebot
from telebot import types
import base64
import time
from fpdf import FPDF
import requests
import pdfkit


bot = telebot.TeleBot("5965917042:AAEeegS2itBOoqeRebv8nUdoDedrTC6QnD0")
pdf = FPDF()




@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Please input the VIN')


@bot.message_handler()
def choose_the_type(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_carfax = types.InlineKeyboardButton(text="Carfax", callback_data='carfax')
    item_autocheck = types.InlineKeyboardButton(text="Autocheck", callback_data='autocheck')

    markup_inline.add(item_autocheck, item_carfax)
    bot.send_message(message.chat.id, "Please choose the report type", reply_markup = markup_inline)




@bot.callback_query_handler(func=lambda call:True)
def answer(call):
    if call.data == "carfax":
        
        data = requests.get("https://api.allreports.tools/wp-json/v1/get_report_by_wholesaler/WAUDG74F25N111998/68523d5476af56837fd1b57c867f2fe9/carfax/ru")
        js = data.json()
        report = js["report"]["report"]
        decoded = base64.b64decode(report)
        html = decoded.decode("UTF-8")
        pdfkit.from_string(html, f'{js["report"]["vin"]}-{js["report"]["id"]}.pdf')
        carfax =  open(f'./{js["report"]["vin"]}-{js["report"]["id"]}.pdf', "rb")
        bot.send_document(call.message.chat.id, carfax)

    elif call.data == "autocheck":
        
        data = requests.get("https://api.allreports.tools/wp-json/v1/get_report_by_wholesaler/WAUDG74F25N111998/68523d5476af56837fd1b57c867f2fe9/autocheck/ru")
        js = data.json()
        report = js["report"]["report"]
        decoded = base64.b64decode(report)
        html = decoded.decode("UTF-8")
        print(html)
        # pdfkit.from_string(html, f'{js["report"]["vin"]}-{js["report"]["id"]}.pdf')
        # time.sleep(3)
        # carfax =  open(f'./{js["report"]["vin"]}-{js["report"]["id"]}.pdf', "rb")
        # bot.send_document(call.message.chat.id, carfax)








    













bot.infinity_polling()