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
#import easygui
import fpdf

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
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
    d = defaultdict(str)
    if(not data):
	return d
    entries = data.split('[')[1].split(']')[0].split('),')
    for entry in entries:
        key = entry.split(',')[0].split('\'')[1]
        val = entry.split(',')[1].split('\'')[1]
        d[key] = val
    return d

# generate a pdf from the json template that provides instructions
def gen_pdf(surg_info, insns):
    month = surg_info[0]
    day = surg_info[1]
    year = surg_info[2]
    pdf = fpdf.FPDF(format='letter')
    pdf.set_auto_page_break(True,margin=0)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(195, 10, txt="Pre-Surgery Instructions", align="C")
    pdf.ln(h='')
    pdf.set_font("Arial", size=10)
    surg_date = datetime.date(year, month, day).strftime("%A, %B %d, %Y")
    intro = "Your surgery is scheduled on " + surg_date + ". You will receive a phone call to tell you what time to arrive at the hospital. If you do not receive a call by noon the day before your surgery, please call the office. If you can't keep your surgery appointment, call your surgeon's office."
    pdf.multi_cell(195, 10, txt=intro, align="L")
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 195, pdf.get_y())
    pdf.ln(h='')

    keys = insns.keys()
    int_keys = []
    for key in keys:
        int_keys.append(int(key))
    sorted_keys = int_keys.sort(reverse=True)
    sorted_str_keys =[]
    for key in int_keys:
        sorted_str_keys.append(str(key))

    # insns = json.loads(insns_json)
    for key in sorted_str_keys:
        insns_for_day = insns[key]
                # date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        # insn_for_pdf["num_days"] = int(i.split(':')[0])
        insn_date = (datetime.date(year, month, day) - datetime.timedelta(int(key))).strftime("%A, %B %d, %Y")
        pdf.set_font("Arial", style="B", size=10)
        pdf.multi_cell(195, 10, txt=insn_date, align="L")
        for indiv_insn in insns_for_day:
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(195, 7, txt=indiv_insn, align="L")
            pdf.set_font("Arial", size=2)
            pdf.multi_cell(195, 5, txt="\n", align="L")
        pdf.multi_cell(195, 5, txt="\n", align="L")

    # pdf.close()
    pdf.output(name="Instructions.pdf", dest="F")
    pdf_string = pdf.output(name="Instructions.pdf", dest="S")
    return pdf_string

def generate_pdf():

    input = get_user_input(flags.data)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

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
    insns_for_pdf = {}
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

        # insn_for_pdf = {}
        # date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        # insn_for_pdf["num_days"] = int(i.split(':')[0])
        # insn_for_pdf["date"] = date.strftime("%A, %B %d, %Y")
        # insn_for_pdf["insn_text"] = cat_insns[insn].split(':')[1]
        # insns_for_pdf.append(insn_for_pdf)

        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        num_days = i.split(':')[0]
        if (num_days in insns_for_pdf):
            insns_for_pdf[num_days].append(cat_insns[insn].split(':')[1])
        else:
            insn_for_pdf = []
            insn_for_pdf.append(cat_insns[insn].split(':')[1])
            insns_for_pdf[num_days] = insn_for_pdf


    # sorted_insns_for_pdf = sorted(insns_for_pdf, key=lambda insn_for_pdf: insn_for_pdf["num_days"], reverse=True)
    surg_info = [int(month), int(day), int(year)]
    # pdf =  gen_pdf(surg_info, json.dumps(sorted_insns_for_pdf))
    pdf =  gen_pdf(surg_info, insns_for_pdf)
    print (pdf)
    return pdf

if __name__ == '__main__':
    generate_pdf()

