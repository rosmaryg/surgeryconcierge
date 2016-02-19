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
import fpdf

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
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
        key = entry.split(',')[0].split('\'')[1]
        val = entry.split(',')[1].split('\'')[1]
        d[key] = val
    return d

# generate a pdf from the json template that provides instructions
def gen_pdf(surg_info, insns_json):
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

    insns = json.loads(insns_json)
    for num in range(len(insns)):
        insn = insns[num]
        pdf.set_font("Arial", style="B", size=10)
        pdf.multi_cell(195, 10, txt=insn["date"], align="L")
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(195, 7, txt=insn["insn_text"], align="L")
        pdf.set_font("Arial", size=2)
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
    insns_for_pdf = []
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

        insn_for_pdf = {}
        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        insn_for_pdf["num_days"] = int(i.split(':')[0])
        insn_for_pdf["date"] = date.strftime("%A, %B %d, %Y")
        insn_for_pdf["insn_text"] = cat_insns[insn].split(':')[1]
        insns_for_pdf.append(insn_for_pdf)

    sorted_insns_for_pdf = sorted(insns_for_pdf, key=lambda insn_for_pdf: insn_for_pdf["num_days"], reverse=True)
    surg_info = [int(month), int(day), int(year)]
    pdf =  gen_pdf(surg_info, json.dumps(sorted_insns_for_pdf))
    print (pdf)
    return pdf

if __name__ == '__main__':
    generate_pdf()

