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

insn_table = {
'0' : "0: Be prepared to spend a full day at the hospital. Wear loose, comfortable clothing and do not bring valuables. Bring a list of all medications you take.",
'1' : "0: Do not wear jewelry, wedding bands, body piercings, makeup, nail polish, artificial nails",
'2' : "0: Do not wear contact lenses",
'3' : "0: Do not eat or drink anything",
'4' : "1: Do not eat or drink anything after midnight (no water, coffee, gum, lifesavers, ice, food, etc.)",
'5' : "0: Take all meds with a sip of water at your usual times (except diabetes meds)",
'6' : "0: Bring the following to the hospital - inhalers, CPAP mask, eye drops",
'7' : "1: Do not drink any alcoholic beverages or smoke 24 hours prior to surgery",
'8' : "14: Stop taking these herbal products, nutritional supplements - ",
'8a' : "Echinacea", 
'8b' : "Ephedra", 
'8c' : "Feverfew", 
'8d' : "Garlic", 
'8e' : "Ginger", 
'8f' : "Ginkgo biloba", 
'8g' : "Ginseng", 
'8h' : "Kava Kava", 
'8i' : "Saw palmetto", 
'8j' : "St. John''s West", 
'8k' : "Fish oil", 
'8l' : "Vitamin B",
'9' : "7: Stop taking all medicines containing aspirin - ", 
'9a' : "Aspirin", 
'9b' : "Anacin", 
'9c' : "Ascriptin", 
'9d' : "Pepto-Bismol", 
'9e' : "Bufferin", 
'9f' : "Alka-Seltzer", 
'9g' : "Excedrin", 
'9h' : "Florinal", 
'9i' : "Lortab ASA",
'10': "7: Stop taking Non-Steroidal Anti-inflammatory Drugs (NSAIDs) - ",
'10a' : "Ibuprofen (Advil Motrin, Nuprin, Medipren)", 
'10b' : "Naproxen (Aleve, Anaprox, Naprosyn)", 
'10c' : "Diclofenac (Cataflam, Voltaren, Arthrotec)", 
'10d' : "Celebrex", 
'10e' : "Toradol (ketorolac)", 
'10f' : "Lodine (etodolac)", 
'10g' : "Feldene (piroxicam)", 
'10h' : "Relefeo (nuburnetce)",
'11': "7: Stop taking Accutane",
'12': "3: Stop taking Suboxone",
'13': "3: Cialis, Viagra, and Levitra",
'14': "5:Stop blood thinner warfarin (Coumadin); switch to Lovenox (enoxaparin) temporarily if advised by doctor",
'15': "7: Stop the following blood thinning medicines - ",
'15a' : "Plavix (Clopidogrel)", 
'15b' : "Xarelto (Rivaroxaban)", 
'15c' : "Ticlid (Ticlopidine)", 
'15d' : "Pletal (Cilostazol)", 
'15e' : "Brilinta (Ticagrelor)", 
'15f' : "Effient (prasugrel)", 
'15g' : "Aggrenox (Aspirin-Dipridarrola)",
'16': "1: Follow instructions from doctor for diabetes",
'17': "0: Do not take any medicine that is a water pill (diuretic) including - ",
'17a' : "furosemide (Lasix)", 
'17b' : "hydrochlorothiazide (HCTZ)", 
'17c' : "medicines combined with hydrochlorothiazide (HCT)"
}

def get_user_input(data):
    entries = data.split('[')[1].split(']')[0].split('),')
    d = defaultdict(str)
    for entry in entries:
        key = entry.split(',')[0].split('\'')[1]
        val = entry.split(',')[1].split('\'')[1]
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
    
    cal['dtstart'] = now.strftime("%Y%m%dT080000")
    cal['summary'] = 'Surgery Concierge'

    print (str(input))

    cat_insns = {}
    for insn in input:
        print (insn)
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

        event = icalendar.Event()
        event.add('dtstart', date.strftime("%Y%m%dT000000"))
        event.add('dtend', end.strftime("%Y%m%dT000000"))
        event.add('summary', cat_insns[insn].split(':')[1])
        cal.add_component(event)
    
    print (cal.to_ical())
    return display(cal)
'''
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
'''

if __name__ == '__main__':
    generate_ics()

