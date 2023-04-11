import telebot
from telebot import types
import base64
import requests
import pdfkit


bot = telebot.TeleBot("5965917042:AAEeegS2itBOoqeRebv8nUdoDedrTC6QnD0")

VIN = 1



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Please input the 17 char VIN')



# ##Getting data##############################
# def getData(message):
#     data = requests.get(
#         f"https://api.allreports.tools/wp-json/v1/get_report_by_wholesaler/{message.text.upper()}/68523d5476af56837fd1b57c867f2fe9/carfax/ru")
#     if data.status_code == 200:
#         js = data.json()
#         report = js["report"]["report"]
#         decoded = base64.b64decode(report)
#         html = decoded.decode("UTF-8")
#         pdfkit.from_string(html, f'{js["report"]["vin"]}-{js["report"]["id"]}.pdf')
#         carfax = open(f'./{js["report"]["vin"]}-{js["report"]["id"]}.pdf', "rb")
#         bot.send_document(message.chat.id, carfax)
#     else:
#         bot.reply_to(message, data.text)



@bot.message_handler()
def answer(message):
   
    if len(message.text) < 17:
        bot.reply_to(message, f'Please input valid VIN code.\n Should be 17 char long!!!!')
    else:

        bot.reply_to(message, f'Please wait, checking the carfax database for records...')
        records = requests.get(f"https://api.allreports.tools/wp-json/v1/get_report_check/{message.text}")
    
        if records.status_code == 200:
            markup_reply = types.InlineKeyboardMarkup()
            get_carfax = types.InlineKeyboardButton(text="Pay and  get Carfax report", callback_data="yes")
            markup_reply.add(get_carfax)

            data = records.json()
            bot.send_message(message.chat.id, f'Found {data["carfax"]["records"]} records in Carfax database: \n model:{data["carfax"]["vehicle"]}', reply_markup=markup_reply)
        else:
            bot.reply_to(message, f'No records found for mentioned VIN!!!!')




@bot.callback_query_handler(func=lambda call: True)
def handle_answer(msg):
        if msg.data == "yes":
            print(VIN)
            data = requests.get(
                f"https://api.allreports.tools/wp-json/v1/get_report_by_wholesaler/{VIN.upper()}/68523d5476af56837fd1b57c867f2fe9/carfax/ru")
            print(data.status_code)
            if data.status_code == 200:
                js = data.json()
                report = js["report"]["report"]
                decoded = base64.b64decode(report)
                html = decoded.decode("UTF-8")
                pdfkit.from_string(html, f'{js["report"]["vin"]}-{js["report"]["id"]}.pdf')
                carfax = open(f'./{js["report"]["vin"]}-{js["report"]["id"]}.pdf', "rb")
                bot.send_document(msg.json.message.chat.id, carfax)
           
    


























bot.infinity_polling()