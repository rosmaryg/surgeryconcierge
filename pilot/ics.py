from __future__ import print_function
import os
import sys
from collections import defaultdict
import icalendar
import datetime
import json
from insns import insn_table

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
    entries = data.split('[')[1].split(']')[0].split('),')
    for entry in entries:
        key = entry.split(',')[0].split('\'')[1].split('\\')[0]
        val = entry.split(',')[1].split('\'')[1].split('\\')[0]
        d[key] = val
    return d

def display(cal):
    return cal.to_ical().replace('\r\n', '\n').strip()

def generate_ics():
    
    input = get_user_input(flags.data)
    now = datetime.datetime.utcnow()

    cal = icalendar.Calendar()
    year = input['year']
    month = input['month']
    day = input['day']
    
    cal['dtstart'] = now.strftime("%Y%m%dT000000")
    cal['summary'] = 'Surgery Concierge'

    cat_insns = {}
    print(input)
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
    for base_insn in cat_insns:
	if base_insn == 'insn10' and not input['insn10']:
		continue
	insn = base_insn[4:]	
        i = insn_table[insn]
        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        end = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))

        event = icalendar.Event()
        event.add('dtstart', date)
        event.add('dtend', end)
	if base_insn != 'insn10':
        	event.add('summary', cat_insns[base_insn].split(':')[1])
	else:
		event.add('summary', input['insn10'])
        cal.add_component(event)
    
    print (cal.to_ical())
    return display(cal)

if __name__ == '__main__':
    generate_ics()

