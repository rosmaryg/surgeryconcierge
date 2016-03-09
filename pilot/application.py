import subprocess
import requests
import json
import datetime
from flask import request
from flask import Flask, render_template, make_response

application = Flask(__name__)

@application.route('/')
def index():
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
  print str(request.args)
  ics = subprocess.check_output(["python", "ics.py", "--data", "\"" + str(request.args) + "\""])
  response = make_response(ics)
  response.headers['Content-Disposition'] = "inline; filename=instructions.ics"
  response.mimetype = 'application/ics'
  return response

@application.route('/generate-pdf')
def genPdf():
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
	url = "http://node.p9s9sjcatq.us-east-1.elasticbeanstalk.com/schedule_texts" 
  	headers = {'content-type': 'application/json'}
  	r = requests.post(url,data=json.dumps(ret_val),headers=headers)
	print r.content
	return "Texts now being sent."
  except subprocess.CalledProcessError:
	return "Error in sending texts. Double check your entered number."


if __name__ == '__main__':
  application.debug = True
  application.run()
