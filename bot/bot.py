import config
import telebot
import db
import time
import ast
from telebot import types

bot = telebot.AsyncTeleBot(config.token)

# for row in db.cursor:
#     print(row)
#
# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message): # Название функции не играет никакой роли
#     bot.send_message(message.chat.id, message.text+str(db.cursor.rowcount))
#
# if __name__ == '__main__':
#      bot.infinity_polling()

def makeKeyboard(stringList):
    markup = types.InlineKeyboardMarkup()
    markup.add( types.InlineKeyboardButton(text=stringList["ans1"], callback_data="['ontest', '1']"),
                types.InlineKeyboardButton(text=stringList["ans2"], callback_data="['ontest', '2']"),
                types.InlineKeyboardButton(text=stringList["ans3"], callback_data="['ontest', '3']"),
                types.InlineKeyboardButton(text=stringList["ans4"], callback_data="['ontest', '4']"))
    return markup

@bot.message_handler(commands=['start'])
def process_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True,True)
    keyboard.row('Математика', 'Історія', 'Інформатика', 'Фізика')
    bot.send_message(message.chat.id, text='Вибери предмет', reply_markup=keyboard)

@bot.message_handler(content_types = ['text'])
def choosePart(message):

        math_1 = telebot.types.InlineKeyboardMarkup()
        math_1.add(telebot.types.InlineKeyboardButton(text="ЗНО1", callback_data="['choosepart', 'zno1']"))
        math_1.add(telebot.types.InlineKeyboardButton(text="ЗНО2", callback_data="['choosepart', 'zno2']"))
        math_1.add(telebot.types.InlineKeyboardButton(text="ЗНО3", callback_data="['choosepart', 'zno3']"))
        math_1.add(telebot.types.InlineKeyboardButton(text="ЗНО4", callback_data="['choosepart', 'zno4']"))
        if message.text == 'Математика':

            bot.send_message(message.chat.id, text='Виберіть розділ', reply_markup=math_1)



@bot.callback_query_handler(func=lambda call: True)
def onTest(call):
    global question, answers

    if call.data.startswith("['choosepart'"):
        acceptboard = telebot.types.InlineKeyboardMarkup()
        acceptboard.add(types.InlineKeyboardButton(text="Почати тестування",
                                                   callback_data="['ontest','0 question']"),
                        types.InlineKeyboardButton(text="Повернутись",
                                                   callback_data="['choosepart']"))
        if ast.literal_eval(call.data)[1] == "zno1":
            config.name = "math"
            db.getTable()
            question = db.question.fetchall()
            answers = db.answers.fetchall()
            config.count = 0
            bot.send_message(call.message.chat.id,
                             text='Ви вибрали розділ ЗНО1',
                             reply_markup=acceptboard)

    if call.data.startswith("['ontest'"):
        print(config.count)
        print(ast.literal_eval(call.data)[1])
        print(str(answers[config.n]["trueans"]))
        if config.n < db.question.rowcount:
            if ast.literal_eval(call.data)[1] == str(answers[config.n]["trueans"]):
                config.count += 1
        if config.n >= db.question.rowcount:
            bot.answer_callback_query(callback_query_id=call.id,
                                      show_alert=True,
                                      text="Тест завершений\nКількість набраних балів:"+str(config.count)+"/"+str(config.n))

        bot.send_message(chat_id=call.message.chat.id,
                         text=question[config.n]["question"],
                         reply_markup=makeKeyboard(answers[config.n]))

        config.n = config.n + 1

while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)