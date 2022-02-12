import datetime
from dateutil.relativedelta import relativedelta

today = datetime.datetime.now().date()

def get_5years_ago(today=today):
    return today + relativedelta(years=-5)

# if __name__ == '__main__':
#     print(str(get_5years_ago()))