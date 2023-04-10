import telebot
from telebot import types
import base64
import json
import requests
import pdfkit


bot = telebot.TeleBot("5965917042:AAEeegS2itBOoqeRebv8nUdoDedrTC6QnD0")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'please input the vlan id')

@bot.message_handler()
def get_user_message(message):
    data = requests.get("https://api.allreports.tools/wp-json/v1/get_report_by_wholesaler/WAUDG74F25N111998/68523d5476af56837fd1b57c867f2fe9/carfax/en")
    js = data.json()
    report = js["report"]["report"]
    decoded = base64.b64decode(report)
    html = decoded.decode("utf-8")
    pdfkit.from_string(html, f'{js["report"]["id"]}.pdf')
    carfax =  open(f'./{js["report"]["id"]}.pdf', "rb")
    bot.send_document(message.chat.id, carfax)

    













bot.infinity_polling()