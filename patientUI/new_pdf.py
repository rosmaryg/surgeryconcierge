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
import fpdf

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('--data', help="User data from html form")
    flags = parser.parse_args()
except ImportError:
    flags = None

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
    intro = "Your surgery is scheduled on " + surg_date + ". You will receive a phone call to tell you what time to arrive at the hospital. If you do not receive a call by 3pm the day before your surgery, please call the office before 4pm. If you can't keep your surgery appointment, call your surgeon's office as soon as possible."
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


def get_user_input(data):
    d = defaultdict(str)
    if(not data):
        return d
    entries = data.split("u'")
    d['insns'] = entries[1].split("')")[0]
    d['date'] = entries[2].split("')")[0]
    return d

def generate_pdf():
    input = get_user_input(flags.data)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    insns = json.loads(input['insns'])
    given_date = input['date']
    given_date_split = given_date.split("/")
    month = given_date_split[0]
    day = given_date_split[1]
    year = given_date_split[2]
    insns_for_pdf = {}
    for key in insns:
        insn = " " + insns[key][0]['insn']
        time = insns[key][1]['time']
        time_unit = insns[key][2]['time_unit']
        if (time_unit == "weeks"):
            time = str(int(time)*7)
            time_unit = "days"
        date = datetime.date(int(year), int(month), int(day)) - datetime.timedelta(int(time))
        if (time in insns_for_pdf):
            insns_for_pdf[time].append(insn)
        else:
            insn_for_pdf = []
            insn_for_pdf.append(insn)
            insns_for_pdf[time] = insn_for_pdf
    # sorted_insns_for_pdf = sorted(insns_for_pdf, key=lambda insn_for_pdf: insn_for_pdf["num_days"], reverse=True)
    surg_info = [int(month), int(day), int(year)]
    # pdf =  gen_pdf(surg_info, json.dumps(sorted_insns_for_pdf))
    pdf =  gen_pdf(surg_info, insns_for_pdf)
    print (pdf)
    return pdf

if __name__ == '__main__':
    generate_pdf()

