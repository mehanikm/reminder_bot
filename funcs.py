from aux import *


def check_date_range(date):
    """Checks if the date is valid"""
    year = int(date.split(".")[-1])
    month = int(date.split(".")[1])
    day = int(date.split(".")[0])
    if year in range(19, 26) and month in range(1, 13) and day in year_f(year + 2000)[month]:
        return True
    return False


def format_date(date: str) -> str:
    """Formats date to DD.MM.YYYY """
    year = date.split(".")[-1]
    month = date.split(".")[1]
    day = date.split(".")[0]
    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month
    year = "20" + year
    return ".".join([day, month, year])


def year_f(y: int) -> dict:
    """Generates dict with
    keys-months and values-lists of its days
    """
    year = {i: [j for j in range(1, 31)] for i in range(1, 13)}
    for i in [1, 3, 5, 7, 8, 10, 12]:
        year[i].append(31)
    if y % 4 == 0:
        year[2].pop()
    elif y % 4 != 0:
        year[2].pop()
        year[2].pop()
    return year


def full_date_check(bot, message, date, users, wday=0):
    chat = message.chat.id
    # Check if date matches to pattern
    if date_pattern.match(date):
        # Chech range of year, month and day of month
        if check_date_range(date):
            bot.send_chat_action(chat, "typing")
            date = format_date(date)
            info = date + ", " * int(bool(wday)) + str(wday)*int(bool(wday))
            newtasks[str(chat)].date = date
            bot.reply_to(
                message, f"Ok! Task planned for *{info}*\n\n" +
                "Now, send me desired time in format    `23:59`",
                parse_mode="Markdown")
            users[str(chat)]["status"] = TIME
        # If year, month or day is out of range, report it to user
        else:
            bot.reply_to(message, "Invalid date range!\n" +
                         "Send me date in format\n`DD.MM.YY`\n" +
                         "where YY must be in range `19-25`!", parse_mode="Markdown")
    # If message does not matches to regexp, report it to user
    else:
        bot.reply_to(message, "Invalid date format!\n" +
                     "Send me date in format\n`DD.MM.YY` " +
                     "where YY must be in range `19-25`!", parse_mode="Markdown")
