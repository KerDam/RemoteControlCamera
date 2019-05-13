from datetime import datetime


def logDate():
    f = open("log.txt", 'a')
    today = datetime.today()
    f.write(today.isoformat()+ "\n")
    f.close()
    return 0


if __name__ == '__main__':
    logDate()
