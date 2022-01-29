import datetime

def get_age(year, month, day):
    today = datetime.date.today()
    birthday = datetime.date(year, month, day)
    return (int(today.strftime("%Y%m%d")) - int(birthday.strftime("%Y%m%d"))) // 10000