from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from re import compile
from datetime import date, timedelta
from time import strftime

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
TEXT = 1
DATE = 2
CDATE = 3  # Custom date set status
TIME = 4

# Date choice keyboard
today = KeyboardButton("Today")
tomorrow = KeyboardButton("Tomorrow")
custom = KeyboardButton("Custom")
keyb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyb.add(today, tomorrow, custom)

# Pattern to match input date
date_pattern = compile(r"^\d{1,2}.\d{1,2}.\d{2}$")

TODAY = ".".join(str(date.today()).split("-")[::-1])
TOMORROW = ".".join(str(date.today() + timedelta(days=1)).split("-")[::-1])
WEEKDAY = strftime("%A")

# New tasks
newtasks = dict()


class Task:
    def __init__(self):
        self.text = ""
        self.date = ""
        self.time = ""
        self.repeat = False
        self.repeats = 0
        self.time_gap = 0  # in minutes

# Users data structure
# users = {user:{status:st, tasks=[]}}
