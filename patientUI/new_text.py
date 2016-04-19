from collections import defaultdict
import datetime
#from apscheduler.schedulers.blocking import BlockingScheduler as Scheduler
from threading import Timer
from twilio.rest import TwilioRestClient
import logging
import json
logging.basicConfig()
try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help="User data from html form")
    flags = parser.parse_args()
except ImportError:
    flags = None

#account_sid = "SK2a72b2e69a384838e82640aa07c2fa3a"
#auth_token = "kRdEtj8xQg1wA4JOc80ZPPN0ddetB743"
account_sid = "ACed13edfc5830a0afca4ede55a98c58f6"
auth_token = "a4998472c39156c3b300302bc9e1be38"
client = TwilioRestClient(account_sid, auth_token)

def send_reminder(text, number):
    message = client.messages.create(body=text, to="" + number, from_="+12155157414")

def get_user_input(data):
    d = defaultdict(str)
    if(not data):
        return d
    entries = data.split("u'")
    d['insns'] = entries[2].split("')")[0]
    d['date'] = entries[3].split("')")[0]
    d['phone-number'] = entries[1].split("')")[0]
    return d


def generate_text():
    input = get_user_input(flags.data)
    number = input['phone-number']
    insns = json.loads(input['insns'])
    given_date = input['date']
    given_date_split = given_date.split("/")
    month = given_date_split[0]
    day = given_date_split[1]
    year = given_date_split[2]
    
    nodes = []
    for key in insns:
        insn = insns[key][0]['insn']
        time = insns[key][1]['time']
        time_unit = insns[key][2]['time_unit']
        if (time_unit == "weeks"):
            time = str(int(time)*7)
            time_unit = "days"
        date = datetime.datetime(int(year), int(month), int(day), 20) - datetime.timedelta(int(time) + 1)
        nodes.append({'number':number, 'message':insn,'date':(date.year, date.month, date.day, date.hour)})
    send_reminder("You are now signed up to receive surgery reminders! Text STOP if you want to unsubscribe from reminders or START if you want to re-subscribe to reminders.", number)
# Texting to the driver
    send_reminder("A user opted to join our system\nNumber: " + str(input['phone-number']), "+14842229088")
    if len(input['phone-number2']) == 17:
        date = datetime.datetime(int(year), int(month), int(day), 20) - datetime.timedelta(1)
        nodes.append({'number':input['phone-number2'], 'message':"This is a reminder to pick up your friend from the hospital", 'date':(date.year, date.month, date.day, date.hour)})
        send_reminder("You are now signed up to receive a reminder to pick up your friend from the hospital.  Text STOP if you want to unsubscribe from reminders or START if you want to re-subscribe to reminders.", input['phone-number2'])
        send_reminder("A user opted their pick-up person into our system\nNumber: " + str(input['phone-number2']), "+14842229088")
    print nodes


if __name__ == '__main__':
    generate_text()