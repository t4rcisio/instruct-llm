
import datetime
from filelock import FileLock

def addLog(logType: str, msg: str):

    lock = FileLock("log" + ".lock")

    with lock:

        log_line = str(datetime.datetime.now()) + "\t\t" + logType + "\t\t" + msg + "\n"

        open("events.log", "a", encoding="UTF-8").write(log_line)


def readLog():

    lock = FileLock("log" + ".lock")

    with lock:

        lines = open("events.log", "r", encoding="UTF-8").readlines()

        return lines