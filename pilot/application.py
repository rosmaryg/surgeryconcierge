import subprocess
import requests
import json
import datetime
from twilio.rest import TwilioRestClient
from flask import request
from flask import Flask, render_template, make_response

application = Flask(__name__)
account_sid = "ACed13edfc5830a0afca4ede55a98c58f6"
auth_token = "a4998472c39156c3b300302bc9e1be38"
client = TwilioRestClient(account_sid, auth_token)

counter = 0

def send_data(timestamp, medium, success):
  message = client.messages.create(body="ID: " + str(counter) + "\nRegistered at: " + str(timestamp) + "\nMedium: " + medium + "\nStatus: " + success, to="+14842229088", from_="+12155157414")

@application.route('/')
def index():
  global counter
  counter+=1
  return render_template('index.html')

@application.route('/generate-calendar')
def genCalendar(): 
  ret_val = subprocess.call(["python", "new_calendar.py", "--data", "\"" + str(request.args) + "\""])
  if ret_val == 0:	
    return 'Calendar succesfully created!   <a href="http://google.com/calendar">View my calendar</a> <br><br> <button onClick=\"window.close()\"">Close window</button>'
  else:
    return 'Calendar not created.'

@application.route('/generate-ics')
def genICS():
  send_data(datetime.datetime.now(), "ICS", "Succeeded")
  print str(request.args)
  ics = subprocess.check_output(["python", "ics.py", "--data", "\"" + str(request.args) + "\""])
  response = make_response(ics)
  response.headers['Content-Disposition'] = "inline; filename=instructions.ics"
  response.mimetype = 'application/ics'
  return response

@application.route('/generate-pdf')
def genPdf():
  send_data(datetime.datetime.now(), "PDF", "Succeeded")
  pdf = subprocess.check_output(["python", "new_pdf.py", "--data", "\"" + str(request.args) + "\""])
  response = make_response(pdf)
  response.headers['Content-Disposition'] = "inline; filename=Instructions.pdf"
  response.mimetype = 'application/pdf'
  return response

@application.route('/generate-text')
def genText():
  try:
  	ret_val = subprocess.check_output(["python", "new_text.py", "--data", "\"" + str(request.args) + "\""])
  #if ret_val and type(ret_val) == type(str()):
	ret_val = eval(ret_val)
	url = "http://node.nrm2vzfc7k.us-east-1.elasticbeanstalk.com/schedule_texts" 
  	headers = {'content-type': 'application/json'}
  	r = requests.post(url,data=json.dumps(ret_val),headers=headers)
	print r.content
    	send_data(datetime.datetime.now(), "Texts", "Succeeded")
	return "Texts now being sent."
  except subprocess.CalledProcessError:
    	send_data(datetime.datetime.now(), "Texts", "Failed")
	return "Error in sending texts. Double check your entered cell phone number and/or the number you indicated for your pick up person."


if __name__ == '__main__':
  application.debug = True
  application.run()
