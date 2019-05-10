from datetime import datetime


def logDate():
    with open("log.txt", 'a') as f:
        today = datetime.today()
        print(today.isoformat(), file=f)
    return 0


if __name__ == '__main__':
    logDate()
