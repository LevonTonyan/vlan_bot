import telebot
from telebot import types
import xlrd


bot = telebot.TeleBot("5965917042:AAEeegS2itBOoqeRebv8nUdoDedrTC6QnD0")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'please input the vlan id')

@bot.message_handler()
def get_user_message(message):

    rb =xlrd.open_workbook('vlans.xls', formatting_info=True)

    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows):
        print(sheet.row_values(rownum ,5 ,6), message.text)






bot.infinity_polling()