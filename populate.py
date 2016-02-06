import datetime
import json
import fpdf

# takes in 2-D array of surgeries and returns json 
def test_surgeries_to_json(results):
	json_prep = []
	for result in results:
		surgery = {}
		surgery["id"] = result[0]
		surgery["surgery_name"] = result[1]
		surgery["month"] = result[2]
		surgery["day"] = result[3]
		surgery["year"] = result[4]
		json_prep.append(surgery)
	return json.dumps(json_prep)

# takes in 2-D array of insns and returns json
def insns_to_json(results):
	json_prep = []
	for result in results:
		insn = {}
		insn["date"] = result[0]
		insn["conditions"] = result[1]
		insn["ask_doctor"] = result[2]
		insn["insn_text"] = result[3]
		json_prep.append(insn)
	return json.dumps(json_prep)

# generate a pdf from the json template that provides instructions
def gen_pdf(surg_info, insns_json):
	surgery_name = surg_info[0]
	month = surg_info[1]
	day = surg_info[2]
	year = surg_info[3]
	pdf = fpdf.FPDF(format='letter')
	pdf.set_auto_page_break(True,margin=0)
	pdf.add_page()
	pdf.set_font("Arial", style="B", size=12)
	pdf.cell(195, 10, txt="Pre-Surgery Instructions", align="C")
	pdf.ln(h='')
	pdf.set_font("Arial", size=10)
	surg_date = datetime.date(year, month, day).strftime("%A, %B %d, %Y")
	intro = "Your surgery is scheduled on " + surg_date + ". You will receive \
	a phone call to tell you what time to arrive at the hospital. If you do not receive a call by noon \
	the day before your surgery, please call the office. If you can't keep your surgery appointment, \
	call your surgeon's office."
 	pdf.multi_cell(195, 10, txt=intro, align="L")
 	pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 195, pdf.get_y())
	pdf.ln(h='')

 	insns = json.loads(insns_json)
 	for num in range(len(insns)):
 		insn = insns[num]
		pdf.set_font("Arial", style="B", size=10)
		pdf.multi_cell(195, 10, txt=insn["date"], align="L")
		pdf.set_font("Arial", size=10)
		pdf.multi_cell(195, 10, txt=insn["insn_text"], align="L")

	pdf.output(name="Instructions.pdf", dest="F")




# function takes in the date of the surgery as three parameters (month, day, year)
def timeline_to_json(month, day, year, results, surgery_name):

	update = {}
	update["surgery_name"] = surgery_name
	surg_date = {}
	surg_date["month"] = month
	surg_date["day"] = day
	surg_date["year"] = year
	update["surgery_date"] = surg_date
	insns = []
	for result in results:
		current = {}
		date = datetime.date(year, month, day) + datetime.timedelta(days=result[0])
		current["date"] = date.strftime("%A, %B %d, %Y")
		current["conditions"] = result[1]
		current["ask_doctor"] = result[2]
		current["insn_text"] = result[3]
		insns.append(current)
	update["insns"] = insns

	# jsonFile = open("populated.json", "w+")
	# jsonFile.write(json.dumps(update))
	# jsonFile.close()

	return json.dumps(update)

def patient_data_to_json(results):
	json_prep = []
	result = results[0]
		patient_data = {}
		patient_data["pdf_link"] = result[0]
		patient_data["cal_link"] = result[1]
		json_prep.append(patient_data)
	return json.dumps(json_prep)




# Test Code

results = [
	[
		-14, 
		"", 
		0, 
		"Stop taking these herbal products, nutritional supplements: Echinacea, Ephedra, Feverfew, Garlic, Ginger, Ginkgo biloba, Ginseng, Kava Kava, Saw palmetto, St. John''s West, Fish oil, Vitamin B"
	],
	[
		-7,
		"",
		0,
		"Stop taking all medicines containing aspirin: Aspirin, Anacin, Ascriptin, Pepto-Bismol, Bufferin, Alka-Seltzer, Excedrin, Florinal, Lortab ASA"
	],
	[
		0,
		"",
		0,
		"An adult will need to pick you up after surgery"
	]
]

insns = [
    {
      "date": "Tuesday, November 03, 2015",
      "conditions": "",
      "ask_doctor": 0,
      "insn_text": "Stop taking these herbal products, nutritional supplements: Echinacea, Ephedra, Feverfew, Garlic, Ginger, Ginkgo biloba, Ginseng, Kava Kava, Saw palmetto, St. John''s West, Fish oil, Vitamin B"
    },
    {
      "date": "Tuesday, November 10, 2015",
      "conditions": "",
      "ask_doctor": 0,
      "insn_text": "Stop taking all medicines containing aspirin: Aspirin, Anacin, Ascriptin, Pepto-Bismol, Bufferin, Alka-Seltzer, Excedrin, Florinal, Lortab ASA"
    },
    {
      "date": "Tuesday, November 17, 2015",
      "conditions": "",
      "ask_doctor": 0,
      "insn_text": "An adult will need to pick you up after surgery"
    }
  ]


# blah = populate(11, 17, 2015, results, "blah")
# print blah
# gen_pdf(blah, 11, 17, 2015, insns)


test_surgeries = [
	[
		0,
		"a",
		10,
		31,
		2015
	],
	[
		1,
		"b",
		01,
		13,
		2017
	],
	[
		3,
		"r",
		07,
		17,
		2016
	]
]

# print test_surgeries_to_json(test_surgeries)
