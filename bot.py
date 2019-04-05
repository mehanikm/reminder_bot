import json
from time import sleep
from datetime import date, timedelta
from re import match

import telebot
from telebot.types import ReplyKeyboardRemove

from config import token
from funcs import *
from aux import *

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
    chat = message.chat.id
    sleep(0.1)
    bot.send_chat_action(chat, 'typing')
    sleep(0.5)
    bot.send_message(chat, 'Here is guide to use me:')
    sleep(0.1)
    bot.send_chat_action(chat, 'typing')
    sleep(0.5)
    bot.send_message(chat, parse_mode="Markdown",
                     text=helpmessage)


# Handle [cancel] command
@bot.message_handler(commands=['cancel'])
def cancel(message):
    chat = message.chat.id
    if users.get(str(chat)).get("status"):
        users[str(chat)]["status"] = NONE
        bot.send_message(
            chat, "`Successfully cancelled current operation!`",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove(selective=True))
    else:
        bot.send_message(chat, "`Nothing to cancel...`", parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove(selective=True))


# Handle [new] command
@bot.message_handler(commands=['new'])
def new_task(message):
    chat = message.chat.id
    bot.reply_to(message, "Great! Now, send me your *task*.",
                 parse_mode="Markdown")
    # Add new task to dict with all users new tasks
    newtasks[str(chat)] = dict(text="", date="", wday="", time="",
                               repeat=False, repeats=0, time_gap=0)
    # Change user's status so he can proceed to next step(Add text)
    users[str(chat)]["status"] = TEXT


# Add task's text
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == TEXT)
def add_text(message):
    chat = message.chat.id
    try:
        # Try to parse message's text to new task
        newtasks[str(chat)]["text"] = message.text
        # Change user's status so he can proceed to next step (Add date)
        users[str(chat)]["status"] = DATE
        bot.reply_to(message, "Now you are can add date to your task!" +
                     f"_Tip: today is {TODAY}, {WEEKDAY}_",
                     reply_markup=keyb, parse_mode="Markdown")
    except:
        bot.send_message(chat, "Send me plain text message, please!")


# Add task's date
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == DATE)
def choose_date(message):
    chat = message.chat.id
    try:
        if "week" in message.text.lower():
            bot.reply_to(message,
                         f"Choose date from below:",
                         reply_markup=week_keyb,
                         parse_mode="Markdown")
            users[str(chat)]["status"] = WDATE
        # If user pressed [custom] button or sent whatever
        else:
            bot.reply_to(message, "Send me desired date in format\n`DD.MM.YY` " +
                         "where YY must be in range `19-25`",
                         reply_markup=ReplyKeyboardRemove(selective=True),
                         parse_mode="Markdown")
            users[str(chat)]["status"] = CDATE
    except:
        bot.send_message(chat, "I can't distinguish that...")


# Add date from reply keyboard
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == WDATE)
def add_date(message):
    try:
        date, wday = message.text.split()[-1], message.text.split()[0][:-1]
        # Checks date's pattern and range
        if date_pattern.match(date) and check_date_range(date):
            bot.send_chat_action(message.chat.id, "typing")
            add_date_to_task(bot, message, date, users, wday)
            bot.reply_to(
                message, f"Ok! Task planned for *{date}, {wday}*\n\n" +
                "Now, select desired hour and minute to get notification!",
                parse_mode="Markdown", reply_markup=hour_keyb)
        # If message does not matches to regexp or smth is out of range, report it to user
        else:
            bot.reply_to(message, "Invalid date format/range!\n" +
                         "Send me date in format\n`DD.MM.YY` " +
                         "where YY must be in range `19-25`!", parse_mode="Markdown")
    # If user sent whatever else, except text, report it to him
    except:
        bot.send_message(message.chat.id, "Choose one option below!",
                         parse_mode="Markdown")

# Add custom task's date
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == CDATE)
def add_custom_date(message):
    try:
        date = message.text
        # Checks date's pattern and range
        if date_pattern.match(date) and check_date_range(date):
            bot.send_chat_action(message.chat.id, "typing")
            add_date_to_task(bot, message, date, users)
            bot.reply_to(
                message, f"Ok! Task planned for *{date}*\n\n" +
                "Now, select desired hour and minute to get notification!",
                parse_mode="Markdown", reply_markup=hour_keyb)
        # If message does not matches to regexp or smth is out of range, report it to user
        else:
            bot.reply_to(message, "Invalid date format/range!\n" +
                         "Send me date in format\n`DD.MM.YY` " +
                         "where YY must be in range `19-25`!", parse_mode="Markdown")
    # If user sent whatever else, except text, report it to him
    except:
        bot.send_message(message.chat.id, "Send me plain text message in format\n" +
                         "`DD.MM.YY`, please!", parse_mode="Markdown")


# Add task's hour
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == HTIME)
def add_hour(message):
    try:
        hour = message.text
        if time_pattern.match(hour) and int(hour) in range(0, 24):
            bot.send_chat_action(message.chat.id, "typing")
            newtasks[str(message.chat.id)]["time"] = hour
            bot.reply_to(message, "Good!\nNow, select minute:",
                         reply_markup=min_keyb)
            users[str(message.chat.id)]["status"] = MTIME
        else:
            bot.reply_to(
                message, "Invalid time format :/\nSend hours in range: 0-23")
    except:
        bot.send_message(
            message.chat.id, "Invalid time format :/\nSend hours in range: 0-23")


# Add task's minute
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == MTIME)
def add_min(message):
    try:
        minute = message.text
        if time_pattern.match(minute) and int(minute) in range(0, 60):
            bot.send_chat_action(message.chat.id, "typing")
            newtasks[str(message.chat.id)]["time"] += ":" + minute
            bot.reply_to(message, "Final time you set for task:\n" +
                         f"*{newtasks.get(str(message.chat.id)).get('time')}*\n\n" +
                         "Now select if to repeat notification.",
                         reply_markup=repeat_keyb, parse_mode="Markdown")
            users[str(message.chat.id)]["status"] = REP
        else:
            bot.reply_to(
                message, "Invalid time format :/\nSend minutes in range: 0-59")
    except:
        bot.send_message(
            message.chat.id, "Invalid time format :/\nSend minutes in range: 0-59")


# Choose if to repeat notification multiple times
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == REP)
def ifrepeat(message):
    try:
        if "yes" in message.text.lower():
            pass  # TODO add case when user wants to repeat notification
            users[str(message.chat.id)]["status"] = REPN
        else:
            bot.reply_to(message, "Ok, just confirm task!\n" +
                         f"Here it is:\n\n*{newtasks[str(message.chat.id)]['text']}*\n" +
                         f"*{newtasks[str(message.chat.id)]['time']}*    " +
                         f"*{newtasks[str(message.chat.id)]['date']}*    " +
                         f"_{newtasks[str(message.chat.id)]['wday']}_",
                         reply_markup=confirm_keyb, parse_mode="Markdown")
            users[str(message.chat.id)]["status"] = FIN
    except:
        bot.send_message(
            message.chat.id, "I can't find answer in your message...")


# Select how many times to repeat
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == REPN)
def repeats(message):
    pass  # TODO Build func to set number of repeats


# Set timegap for repeats
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == TGAP)
def timegap(message):
    pass  # TODO Build func to set timegap for repeats


# Confirmation
@bot.message_handler(func=lambda message:
                     users.get(str(message.chat.id)).get("status") == FIN)
def confirm(message):
    try:
        if "confirm" in message.text.lower():
            users[str(message.chat.id)]["tasks"].append(
                newtasks[str(message.chat.id)])
            newtasks.pop(str(message.chat.id), "")
            users[str(message.chat.id)]["status"] = NONE
            bot.reply_to(message, "Well done!\nSuccessfully added new task to your list!\n" +
                         "Use /list to list all your tasks.", reply_markup=ReplyKeyboardRemove(selective=True))
        else:
            bot.reply_to(message, "Okay, I cancelled your task...", parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove(selective=True))
    except:
        pass  # TODO Write exepct case for this handler


# Handle [list] command
@bot.message_handler(commands=['list'])
def list_tasks(message):
    if not users[str(message.chat.id)]["tasks"]:
        bot.send_message(
            message.chat.id, "`Your tasklist is empty...`", parse_mode="Markdown")

    mess = ""
    for task in users[str(message.chat.id)]["tasks"]:
        mess += f"*{task['text']}*\n" +\
            f"*{task['time']}*    " +\
            f"*{task['date']}*    " +\
            f"_{task['wday']}_"+"\n\n"
    bot.send_message(message.chat.id, mess, parse_mode="Markdown")


# Handle [del] command
@bot.message_handler(commands=['del'])
def del_task(message):
    pass  # TODO Build func to let user to delete tasks

# TODO Build func to delete tasks if expired


if __name__ == '__main__':
    # Open users base
    with open("dump.json") as f:
        users = json.load(f)

    # Start bot's polling
    try:
        bot.polling(none_stop=True)
    # Save users base on stop
    finally:
        for user in users:
            users[user]["status"] = NONE
        with open("dump.json", "w+") as f:
            json.dump(users, f)
