import pandas
import telebot
import sqlite3
import random
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

hello_dict = {1 : "Привет!\U0001F600 \nДавай познакомимся? Меня зовут WordOfTheDayBot! Я здесь для того, чтобы расширить твой словарный запас. \nВот мои команды:\n/start - начало работы\n/help - я покажу тебе снова мои команды\n/delete - если захочешь покинуть меня\n/new - прислать новое слово для запоминания", 2 : "\U0001F913Вот мои команды:\n/start - начало работы\n/help - я покажу тебе снова мои команды\n/delete - если захочешь покинуть меня\n/new - прислать новое слово для запоминания"}
df = pandas.read_csv(config.OUTPUT_CSV)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, hello_dict[1])
    #создаем БД users.bd
    connect = sqlite3.connect('users.bd')
    cursor = connect.cursor()
    #создаем таблицу из одного столбца с id пользователя
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
        id INTEGER
    )""")
    connect.commit()

    #проверяем, есть ли такой пользователь в БДБ чтобы не добавлять его в таблицу второй раз
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
        connect.commit()
    else:
        bot.send_message(message.chat.id, 'Такой пользователь уже существует')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, hello_dict[2])

@bot.message_handler(commands=['new'])
def send_word(message):
    num = random.randrange(0, 996)
    bot.reply_to(message,
                 df.iloc[num, 0].title() + ' ' + '-' + ' ' + df.iloc[num, 1].lower())

@bot.message_handler(commands=['delete'])
def delete(message):
    connect = sqlite3.connect('users.bd')
    cursor = connect.cursor()
    people_id = message.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE  id = {people_id}")
    connect.commit()

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, hello_dict[2])

bot.polling()