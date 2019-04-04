import telebot
from time import sleep
from config import *

# Initialize bot with given token
bot = telebot.TeleBot(token)


# Handle [start] command
@bot.message_handler(commands=['start'])
def start(message):
    sleep(0.5)
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.send_message(message.chat.id, 'Text after start command')


# Handle [help] command
@bot.message_handler(commands=['help'])
def help(message):
    sleep(0.5)
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.send_message(message.chat.id, 'Text after help command')


# Handle [new] command
@bot.message_handler(commands=['new'])
def new_task(message):
    pass


# Handle [list] command
@bot.message_handler(commands=['list'])
def list_tasks(message):
    pass


# Handle [del] command
@bot.message_handler(commands=['del'])
def del_task(message):
    pass


# Start bot's polling
if __name__ == '__main__':
    bot.polling(none_stop=True)
