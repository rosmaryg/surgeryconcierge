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
        key = entry.split(',')[0].split('\'')[1].split('\\')[0]
        val = entry.split(',')[1].split('\'')[1].split('\\')[0]
        d[key] = val
    return d

def split_len(s,block_size):
    w=[]
    n=len(s)
    for i in range(0,n,block_size):
        w.append(s[i:i+block_size])
    return w

def first_text(indiv_insn):
    if len(indiv_insn) < 110:
        return indiv_insn
    else:
        return indiv_insn[0:118]

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
            pdf.rect(pdf.get_x() + 1, pdf.get_y(), 3, 3)
            # pdf.multi_cell(195, 7, txt=indiv_insn, align="L")
            split_insn = split_len(indiv_insn[118:], 113)
            pdf.text(pdf.get_x() + 4, pdf.get_y() + 3, txt=first_text(indiv_insn))
            pdf.multi_cell(195, 5, txt="\n", align="L")
            for text in split_insn:
                pdf.text(pdf.get_x() + 9, pdf.get_y() + 3, txt=text)
                pdf.multi_cell(195, 5, txt="\n", align="L")
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

        # insn_for_pdf = {}
        # date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        # insn_for_pdf["num_days"] = int(i.split(':')[0])
        # insn_for_pdf["date"] = date.strftime("%A, %B %d, %Y")
        # insn_for_pdf["insn_text"] = cat_insns[insn].split(':')[1]
        # insns_for_pdf.append(insn_for_pdf)

        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(i.split(':')[0]))
        num_days = i.split(':')[0]
        if (num_days in insns_for_pdf):
            if base_insn != 'insn10':
                insns_for_pdf[num_days].append(cat_insns[base_insn].split(':')[1])
            else:
                insns_for_pdf[num_days].append(input['insn10'])          
        else:
            insn_for_pdf = []
            if base_insn != 'insn10':
                insn_for_pdf.append(cat_insns[base_insn].split(':')[1])
            else:
                insn_for_pdf.append(input['insn10'])
            insns_for_pdf[num_days] = insn_for_pdf


    # sorted_insns_for_pdf = sorted(insns_for_pdf, key=lambda insn_for_pdf: insn_for_pdf["num_days"], reverse=True)
    surg_info = [int(month), int(day), int(year)]
    # pdf =  gen_pdf(surg_info, json.dumps(sorted_insns_for_pdf))
    pdf =  gen_pdf(surg_info, insns_for_pdf)
    print (pdf)
    return pdf

if __name__ == '__main__':
    generate_pdf()

