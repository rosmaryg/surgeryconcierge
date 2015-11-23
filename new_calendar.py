# invode with python new_calendar.py -i <input>.json -y YYYY -m MM -d DD

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import json
from optparse import OptionParser

#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python for Surgery Concierge'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():

    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-i", "--input",
                      action="store",
                      dest="json_file",
                      default="template.json",
                      help="JSON with events to be added")
    parser.add_option("-y", "--year",
                      action="store",
                      dest="year",
                      default="2017",
                      help="year of surgery",)
    parser.add_option("-m", "--month",
                      action="store",
                      dest="month",
                      default="01",
                      help="month of surgery",)
    parser.add_option("-d", "--day",
                      action="store",
                      dest="day",
                      default="01",
                      help="day of surgery",)
    (options, args) = parser.parse_args()
    option_dict = vars(options)

    """
    1. Creates a Google Calendar API service object.
    2. Creates a new Google Calendar.
    3. Adds surgery events to the calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
 
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    print ('Existing Calendars')
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print (calendar_list_entry['summary'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    calendar = {
        'summary': 'Surgery Concierge',
        'timeZone': 'America/New_York'
    }

    print ('--------')
    created_calendar = service.calendars().insert(body=calendar).execute()
    print ('Surgery Concierge created with Calendar ID ' + created_calendar['id'])

    with open(option_dict['json_file']) as data_file:    
        data = json.load(data_file)

    year = option_dict['year']
    month = option_dict['month']
    day = option_dict['day']
    for entry in data:
        date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(int(entry['days_offset']))
        end = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(int(entry['days_offset']) + 1)
        event = {
          'summary': 'Surgery Concierge',
          'description': entry['insn_text'],
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

        event = service.events().insert(calendarId=created_calendar['id'], body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    main()
