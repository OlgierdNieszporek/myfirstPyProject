import datetime


def get_time():
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y, %H:%M:%S")
    print(now)
    return now
