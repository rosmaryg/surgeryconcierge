import datetime
import json

# function takes in the date of the surgery as three parameters (month, day, year)
def populate(month, day, year, file_directory):

	json_data=open(file_directory).read()
	data = json.loads(json_data)
	#print data
	update = []
	for val in data:
		current = {}
		date = datetime.date(year, month, day) + datetime.timedelta(days=val['days_offset'])
		current["date"] = str(date)
		current["conditions"] = val["conditions"]
		current["ask_doctor"] = val["ask_doctor"]
		current["insn_text"] = val["insn_text"]
		update.append(current)

	jsonFile = open("populated.json", "w+")
	jsonFile.write(json.dumps(update))
	jsonFile.close()


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
populate(11, 17, 2015, "./template.json")