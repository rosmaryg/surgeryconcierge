from collections import defaultdict
import datetime
from twilio.rest import TwilioRestClient
from insns import insn_table, default_insns
try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help="User data from html form")
    flags = parser.parse_args()
except ImportError:
    flags = None

account_sid = "AC993d85892ae868d46074d1629efa2dc2"
auth_token = "7ebc350c70162239eaf85bd2a4a56b70"
client = TwilioRestClient(account_sid, auth_token)


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
    now = datetime.datetime.utcnow()
    
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
    for base_insn in cat_insns:
	if base_insn == 'insn10' and not input['insn10']:
		continue
	insn = base_insn[4:]	
        i = insn_table[insn]
        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        end = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
	#Where we should send a text reminder during x date and time
#	if base_insn != 'insn10':
 #       	event.add('summary', cat_insns[base_insn].split(':')[1])
#	else:
#		event.add('summary', input['insn10']) 
    message = client.messages.create(body="testing button hit", 
	to="+18082379659",
	from_="+12245889141")
'''        event.add('dtstart', date)
        event.add('dtend', end)
        event.add('summary', cat_insns[insn].split(':')[1])
''' 
    for insn in default_insns:
        i = default_insns[insn]
        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        end = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
	#Where we should send a text reminder during x date and time
 #       event.add('summary', i.split(':')[1])
    #message = client.messages.create(body="testing button hit", 
#	to="+18082379659",
#	from_="+12245889141")
'''        event.add('dtstart', date)
        event.add('dtend', end)
        event.add('summary', cat_insns[insn].split(':')[1])
''' 


if __name__ == '__main__':
    generate_text()

