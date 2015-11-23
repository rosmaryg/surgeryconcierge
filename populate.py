import datetime
import json

# function takes in the date of the surgery as three parameters (month, day, year)
def populate(month, day, year, results, surgery_type, query_type):

	update = []
	update.append({"surgery_type": surgery_type})
	update.append({"query_type": query_type})
	for result in results:
		current = {}
		date = datetime.date(year, month, day) + datetime.timedelta(days=result[0])
		current["date"] = str(date)
		current["conditions"] = result[1]
		current["ask_doctor"] = result[2]
		current["insn_text"] = result[3]
		update.append(current)

	# jsonFile = open("populated.json", "w+")
	# jsonFile.write(json.dumps(update))
	# jsonFile.close()

	return json.dumps(update)


	#t = datetime.date(year, month, day)
	#print t
	#print 'day, month, year:', t.day, t.month, t.year


'''
	one_day_prior = t - datetime.timedelta(days=1)
	print 'one      day, month, year:', one_day_prior.day, one_day_prior.month, one_day_prior.year
	two_days_prior = t - datetime.timedelta(days=2)
	print 'two      day, month, year:', two_days_prior.day, two_days_prior.month, two_days_prior.year
	seven_days_prior = t - datetime.timedelta(days=7)
	print 'seven    day, month, year:', seven_days_prior.day, seven_days_prior.month, seven_days_prior.year
	fourteen_days_prior = t - datetime.timedelta(days=14)
	print 'fourteen day, month, year:', fourteen_days_prior.day, fourteen_days_prior.month, fourteen_days_prior.year
	twenty_days_prior = t - datetime.timedelta(days=20)
	print 'twenty   day, month, year:', twenty_days_prior.day, twenty_days_prior.month, twenty_days_prior.year
'''


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

# print populate(11, 17, 2015, results, "blah", "blahblah")
