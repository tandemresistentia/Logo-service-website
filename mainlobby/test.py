import time

def minute_passed(oldepoch):
    return time.time() - oldepoch >= 10

minute_passed(10)