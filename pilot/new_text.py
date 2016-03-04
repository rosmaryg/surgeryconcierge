from collections import defaultdict
import datetime
#from apscheduler.schedulers.blocking import BlockingScheduler as Scheduler
from threading import Timer
from twilio.rest import TwilioRestClient
from insns import insn_table, default_insns
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
account_sid = "AC993d85892ae868d46074d1629efa2dc2"
auth_token = "7ebc350c70162239eaf85bd2a4a56b70"
client = TwilioRestClient(account_sid, auth_token)

def send_reminder(text, number):
    print "sending message: " + text + " to " + str(number)
    message = client.messages.create(body=text, to="+" + number, from_="+12245889141")

def get_user_input(data):
    d = defaultdict(str)
    if(not data):
	return d	
    entries = data.split('[')[1].split(']')[0].split('),')
    for entry in entries:
        key = entry.split(',')[0].split('\'')[1].split('\\')[0]
        val = entry.split(',')[1].split('\'')[1].split('\\')[0]
        d[key] = val
    return d


def generate_text():
    input = get_user_input(flags.data)
    if not 'phone-number' in input:
	return 1
    number = input['phone-number']
    year = input['year']
    month = input['month']
    day = input['day']

    cat_insns = {}
    for insn in input:
        if 'insn' in insn and not insn[-1].isalpha():
            cat_insns[insn] = insn_table[insn[4:]]
    for insn in input:
	if 'insn' in insn and insn[-1].isalpha(): 
		base_insn = insn[:-1]
		if not base_insn in cat_insns:
			cat_insns[base_insn] = insn_table[base_insn[4:]]	
		current_str = cat_insns[base_insn]
		if current_str[-1] != ' ':
	    		cat_insns[base_insn] = current_str + ', ' + insn_table[input[insn]]	
		else:
	    		cat_insns[base_insn] = current_str + insn_table[input[insn]]
    nodes = []
    for base_insn in cat_insns:
	if base_insn == 'insn10' and not input['insn10']:
		continue
	insn = base_insn[4:]	
        i = insn_table[insn]
	date = datetime.datetime(int(year), int(month), int(day), 20) - datetime.timedelta(int(i.split(':')[0]))
	reminder_text = ""
	if base_insn != 'insn10':
        	reminder_text = i.split(':')[1]
	else:
		reminder_text = input['insn10']
	nodes.append({'number':number, 'message':reminder_text,'date':(date.year, date.month, date.day, date.hour)}) 
    for insn in default_insns:
        i = default_insns[insn]
	date = datetime.datetime(int(year), int(month), int(day), 20) - datetime.timedelta(int(i.split(':')[0]))
        reminder_text = i.split(':')[1]
	nodes.append({'number':number, 'message':reminder_text,'date':(date.year, date.month, date.day, date.hour)}) 
#    send_reminder("You are now signed up to receive surgery reminders! Text STOP if you want to unsubscribe from reminders or START if you want to re-subscribe to reminders.", number)
    print {'messages':nodes}


if __name__ == '__main__':
    generate_text()

