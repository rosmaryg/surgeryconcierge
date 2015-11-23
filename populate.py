import datetime
import json
import fpdf


# generate a pdf from the json template that provides instructions
def gen_pdf(surgery_name, month, day, year, insns):
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

 	insns = insns
 	for num in range(len(insns)):
 		insn = insns[num]
		pdf.set_font("Arial", style="B", size=10)
		pdf.multi_cell(195, 10, txt=insn["date"], align="L")
		pdf.set_font("Arial", size=10)
		pdf.multi_cell(195, 10, txt=insn["insn_text"], align="L")

	pdf.output("Instructions.pdf")




# function takes in the date of the surgery as three parameters (month, day, year)
def populate(month, day, year, results, surgery_name):

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


blah = populate(11, 17, 2015, results, "blah")
print blah
gen_pdf(blah, 11, 17, 2015, insns)