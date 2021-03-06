from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from re import compile
from datetime import date, timedelta
from time import strftime, localtime, time

helpmessage = "Firstly, send me /new command.\n" +\
    "I will reply to your command and guide you:\n\n" +\
    "Your first message after /new command is your Task itself.\n\n" +\
    "After adding your reminders's text, you choose date: " +\
    "*today*, *tomorrow* or *custom* in format    `DD.MM.YY`\n\n" +\
    "Next you should send me desired time " +\
    "in format    `23:59`\n\n" + \
    "Next step: you choose how many times " + \
    "should I remind you this task and time gap " + \
    "between repeats _(Maximum: 4 times with 60 min gap)_\n\n" + \
    "That's all! By this time I will only ask you to confirm task!"

# Available status
NONE = 0
TEXT = 1  # Set task's text
DATE = 2  # Set task's date
WDATE = 3  # This week dates
CDATE = 4  # Custom date set
HTIME = 5  # Set hour
MTIME = 6  # Set minute
REP = 7  # Choose if to repeat
REPN = 8  # Select number of repeats
TGAP = 9  # Select time gap for repeats
FIN = 10  # Confirm task and finish

# Date choice keyboard
thisweek = KeyboardButton("This week")
custom = KeyboardButton("Custom")
keyb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyb.add(thisweek, custom)

# Weekdays keyb
week_keyb = ReplyKeyboardMarkup(resize_keyboard=True)
for i in range(8):
    week_keyb.add(KeyboardButton(
        strftime("%A, %d.%m.%y", localtime(time() + 3600 * 24*i))))

# Hour keyboard
hour_keyb = ReplyKeyboardMarkup(resize_keyboard=True)
row = []
for i in range(24):
    i = str(i)
    if len(i) == 1:
        i = "0" + i
    row.append(KeyboardButton(i))
    if len(row) == 3:
        hour_keyb.add(*row)
        row.clear()

# Minutes keyboard
min_keyb = ReplyKeyboardMarkup(resize_keyboard=True)
row = []
for i in range(60):
    i = str(i)
    if len(i) == 1:
        i = "0" + i
    row.append(KeyboardButton(i))
    if len(row) == 6:
        min_keyb.add(*row)
        row.clear()

# Repeat keyboard
repeat_keyb = ReplyKeyboardMarkup()
repeat_keyb.add(KeyboardButton("Yes"), KeyboardButton("No"))

# Confirm keyboard
confirm_keyb = ReplyKeyboardMarkup()
confirm_keyb.add(KeyboardButton("Confirm"), KeyboardButton("Cancel"))


# Pattern to match input date, time
date_pattern = compile(r"^\d{1,2}.\d{1,2}.\d{2}$")
time_pattern = compile(r"^\d{2}$")

TODAY = ".".join(str(date.today()).split("-")[::-1])
TOMORROW = ".".join(str(date.today() + timedelta(days=1)).split("-")[::-1])
WEEKDAY = strftime("%A")

# New tasks
newtasks = dict()


# Users data structure
# users = {user:{status:st, tasks=[]}}
