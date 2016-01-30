from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import json
import easygui

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

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

def generate_calendar():
    """
    1. Creates a Google Calendar API service object.
    2. Creates a new Google Calendar.
    3. Adds surgery events to the calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
 
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

    json_file = easygui.enterbox(
        msg="Please enter the key given to you by your scheduler.",
        title="Surgery Concierge",
        strip=True,
        default="Template JSON name (for now)")
    with open(json_file) as data_file:
        data = json.load(data_file)

    year = easygui.enterbox(
        msg="Year of procedure:",
        title="Surgery Concierge",
        strip=True,
        default="YYYY")
    month = easygui.enterbox(
        msg="Month of procedure:",
        title="Surgery Concierge",
        strip=True,
        default="MM")
    day = easygui.enterbox(
        msg="Day of procedure",
        title="Surgery Concierge",
        strip=True,
        default="DD")

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

        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    generate_calendar()
