def check_date_range(message):
    """Checks if the date is valid"""
    year = int(message.text.split(".")[-1])
    month = int(message.text.split(".")[1])
    day = int(message.text.split(".")[0])
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
