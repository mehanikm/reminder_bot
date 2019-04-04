import telebot
import json
from time import sleep
from config import *

# Initialize bot with given token
bot = telebot.TeleBot(token)


# Handle [start] command
@bot.message_handler(commands=['start'])
def start(message):
    chat = message.chat.id
    # Greet user
    sleep(0.1)
    bot.send_chat_action(chat, 'typing')
    sleep(0.5)
    bot.send_message(chat, f'Hey, {message.from_user.first_name}!')
    sleep(0.1)
    bot.send_chat_action(chat, 'typing')
    sleep(0.5)

    # If really new user, add him to base
    if str(chat) not in users:
        users[str(chat)] = dict()
        users[str(chat)]["status"] = 0
        users[str(chat)]["tasks"] = []
        bot.send_message(
            chat, "I've added you to my users database!")
    else:
        bot.send_message(
            chat, 'You are already in my base of users!')


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
    newtask = dict()


# Add task text
@bot.message_handler(func=lambda message:
                     users_status.get(message.chat.id) == TEXT)
def add_text(message):
    pass


# Handle [list] command
@bot.message_handler(commands=['list'])
def list_tasks(message):
    pass


# Handle [del] command
@bot.message_handler(commands=['del'])
def del_task(message):
    pass


if __name__ == '__main__':
    # Open users base
    with open("dump.json") as f:
        users = json.load(f)

    # Start bot's polling
    try:
        bot.polling(none_stop=True)
    # Save users base on stop
    finally:
        with open("dump.json", "w+") as f:
            json.dump(users, f)
