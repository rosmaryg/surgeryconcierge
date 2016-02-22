from __future__ import print_function
import httplib2
import os
import sys
from collections import defaultdict
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from insns import insn_table
import datetime
import json

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('--data', help="User data from html form")
    flags = parser.parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python for Surgery Concierge'

def get_credentials():
    credential_path = os.path.join(os.getcwd(), 'calendar-python.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
    os.remove(credential_path)
    return credentials

def get_user_input(data):
    d = defaultdict(str)
    if(not data):
	return d
    entries = data.split('[')[1].split(']')[0].split('),')
    for entry in entries:
        key = entry.split(',')[0].split('\'')[1]
        val = entry.split(',')[1].split('\'')[1]
        d[key] = val
    return d

def generate_calendar():
    """
    1. Creates a Google Calendar API service object.
    2. Creates a new Google Calendar.
    3. Adds surgery events to the calendar.
    """
    print "generate calendar!"
    credentials = get_credentials()
    print "got credentials"
    http = credentials.authorize(httplib2.Http())
    print "http through"
    service = discovery.build('calendar', 'v3', http=http)
 
    
    input = get_user_input(flags.data)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    page_token = None
    calendar_id = None

    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == 'Surgery Concierge':
                calendar_id = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    if calendar_id is None:
        calendar = {
            'summary': 'Surgery Concierge',
            'timeZone': 'America/New_York'
            }
        created_calendar = service.calendars().insert(body=calendar).execute()
        print ('Surgery Concierge created with Calendar ID ' + created_calendar['id'])
        calendar_id = created_calendar['id']

#     json_file = easygui.enterbox(
#         msg="Please enter the key given to you by your scheduler.",
#         title="Surgery Concierge",
#         strip=True,
#         default="Template JSON name (for now)")
#     with open(json_file) as data_file:
#         data = json.load(data_file)

    year = input['year']
    '''
    if input['month'] == "":
        month = easygui.enterbox(
            msg="Month of procedure:",
            title="Surgery Concierge",
            strip=True,
            default="MM")
    else:
        month = input['month']

    if input['day'] == "":
        day = easygui.enterbox(
            msg="Day of procedure",
            title="Surgery Concierge",
            strip=True,
            default="DD")
    else:
        day = input['day']
    '''
    month = input['month']
    day = input['day']

    cat_insns = {}
    #Create a dict for the beginning of multi-part insns
    for insn in input:
	if 'insn' in insn and not insn[-1].isalpha():
		cat_insns[insn] = insn_table[input[insn]]
    for insn in input:
	if 'insn' in insn and insn[-1].isalpha(): 
		base_insn = insn[:-1]
		current_str = cat_insns[base_insn]
		if current_str[-1] != ' ':
	    		cat_insns[base_insn] = current_str + ', ' + insn_table[input[insn]]	
		else:
	    		cat_insns[base_insn] = current_str + insn_table[input[insn]]
	
    for insn in input:
        if 'insn' not in insn or insn[-1].isalpha():
            continue
        i = insn_table[input[insn]]
        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        end = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        event = {
          'summary': 'Surgery Concierge',
          'description': cat_insns[insn].split(':')[1],
          'start': {
            'date': str(date),
            'timeZone': 'America/New_York'
          },
          'end': {
            'date': str(end),
            'timeZone': 'America/New_York'
          },
          'reminders': {
            'useDefault': False,
            'overrides': [ # reminders sent at 8pm the day before
              {'method': 'email', 'minutes': 4 * 60},
              {'method': 'popup', 'minutes': 4 * 60},
            ],
          },
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    generate_calendar()

