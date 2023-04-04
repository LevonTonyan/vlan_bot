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
        row = str(sheet.row_values(rownum, 1, 2)[0]).split(",")
        if len(row) > 1:
            for i in row:
                if i == message.text:
                    bot.reply_to(message, sheet.row_values(rownum, 0, 1)[0])
                    break
        elif row[0].split(".")[0] == message.text:
            bot.reply_to(message, sheet.row_values(rownum, 0, 1)[0])
            break














bot.infinity_polling()