from __future__ import print_function
import os
import sys
from collections import defaultdict
import icalendar
import datetime
import json

try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help="User data from html form")
    flags = parser.parse_args()
except ImportError:
    flags = None

def get_user_input(data):
    d = defaultdict(str)
    if(not data):
        return d
    entries = data.split("u'")
    d['insns'] = entries[1].split("')")[0]
    d['date'] = entries[2].split("')")[0]
    return d

def display(cal):
    return cal.to_ical().replace('\r\n', '\n').strip()

def generate_ics():
    
    input = get_user_input(flags.data)
    now = datetime.datetime.utcnow()

    cal = icalendar.Calendar()
    insns = json.loads(input['insns'])
    given_date = input['date']
    given_date_split = given_date.split("/")
    month = given_date_split[0]
    day = given_date_split[1]
    year = given_date_split[2]

        
    cal['dtstart'] = now.strftime("%Y%m%dT000000")
    cal['summary'] = 'Surgery Concierge'

    for key in insns:
        insn = insns[key][0]['insn']
        time = insns[key][1]['time']
        time_unit = insns[key][2]['time_unit']
        if (time_unit == "weeks"):
            time = str(int(time)*7)
            time_unit = "days"
        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(time))
        end = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(time))

        event = icalendar.Event()
        event.add('dtstart', date)
        event.add('dtend', end)
    	event.add('summary', insn)
        cal.add_component(event)
   
    print (cal.to_ical())
    return display(cal)

if __name__ == '__main__':
    generate_ics()

