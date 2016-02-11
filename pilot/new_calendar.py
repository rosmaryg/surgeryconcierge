from __future__ import print_function
import httplib2
import os
import sys
from collections import defaultdict
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import json
import easygui

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

insn_table = {
'0' : "0: Be prepared to spend a full day at the hospital. Wear loose, comfortable clothing and do not bring valuables. Bring a list of all medications you take.",
'1' : "0: Do not wear jewelry, wedding bands, body piercings, makeup, nail polish, artificial nails",
'2' : "0: Do not wear contact lenses",
'3' : "0: Do not eat or drink anything",
'4' : "1: Do not eat or drink anything after midnight (no water, coffee, gum, lifesavers, ice, food, etc.)",
'5' : "0: Take all meds with a sip of water at your usual times (except diabetes meds)",
'6' : "0: Bring the following to the hospital: inhalers, CPAP mask, eye drops",
'7' : "1: Do not drink any alcoholic beverages or smoke 24 hours prior to surgery",
'8' : "14: Stop taking these herbal products, nutritional supplements: Echinacea, Ephedra, Feverfew, Garlic, Ginger, Ginkgo biloba, Ginseng, Kava Kava, Saw palmetto, St. John''s West, Fish oil, Vitamin B",
'9' : "7: Stop taking all medicines containing aspirin: Aspirin, Anacin, Ascriptin, Pepto-Bismol, Bufferin, Alka-Seltzer, Excedrin, Florinal, Lortab ASA",
'10': "7: Stop taking Non-Steroidal Anti-inflammatory Drugs (NSAIDs): Ibuprofen (Advil Motrin, Nuprin, Medipren), Naproxen (Aleve, Anaprox, Naprosyn), Diclofenac (Cataflam, Voltaren, Arthrotec), Celebrex, Toradol (ketorolac), Lodine (etodolac), Feldene (piroxicam), Relefeo (nuburnetce)",
'11': "7: Stop taking Accutane",
'12': "3: Stop taking Suboxone",
'13': "3: Cialis, Viagra, and Levitra",
'14': "5:Stop blood thinner warfarin (Coumadin); switch to Lovenox (enoxaparin) temporarily if advised by doctor",
'15': "7: Stop the following blood thinning medicines: Plavix (Clopidogrel), Xarelto (Rivaroxaban), Ticlid (Ticlopidine), Pletal (Cilostazol), Brilinta (Ticagrelor), Effient (prasugrel), Aggrenox (Aspirin-Dipridarrola)",
'16': "1: Follow instructions from doctor for diabetes",
'17': "0: Do not take any medicine that is a water pill (diuretic); includes furosemide (Lasix), hydrochlorothiazide (HCTZ), and medicines combined with hydrochlorothiazide (HCT)"
}

def get_credentials():
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

def get_user_input(data):
    entries = data.split('[')[1].split(']')[0].split('),')
    d = defaultdict(str)
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
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
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

    for insn in input:
        if 'insn' not in insn:
            continue
        i = insn_table[input[insn]]
        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        end = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        event = {
          'summary': 'Surgery Concierge',
          'description': i.split(':')[1],
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

