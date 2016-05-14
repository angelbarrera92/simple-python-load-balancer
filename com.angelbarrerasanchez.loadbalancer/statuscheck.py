from datetime import datetime
import mongostore

def tick():
    print('Tick! The time is: %s' % datetime.now())