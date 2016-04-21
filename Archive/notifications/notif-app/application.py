from flask import Flask
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import TwilioRestClient
from datetime import datetime
from datetime import timedelta
import json
import logging
import re
logging.basicConfig()

application = Flask(__name__)
scheduler = BackgroundScheduler(timezone='EST')
templist = []

#account_sid = "SK2a72b2e69a384838e82640aa07c2fa3a"
#auth_token = "kRdEtj8xQg1wA4JOc80ZPPN0ddetB743"
account_sid = "AC993d85892ae868d46074d1629efa2dc2"
auth_token = "7ebc350c70162239eaf85bd2a4a56b70"
client = TwilioRestClient(account_sid, auth_token)


import os, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from time import strftime
my_email = "virtual.surgery.concierge@gmail.com"
to_email = "tadas412@gmail.com"
my_pass = "cis401concierge"

def sendEmail(subject, message):
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = to_email
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_email, my_pass)
    text = msg.as_string()
    server.sendmail(my_email, to_email, text)
    server.quit()

@application.route('/')
def homepage():
    return "Notifications Node Homepage."

@application.route('/view_jobs', methods=['GET'])
def view_jobs():
    jobs = scheduler.get_jobs()
    st = 'TEXTS SCHEDULED...<br><br><br>'
    for job in jobs:
        job_s = 'Text: ' + job.args[0] + '<br>Number: ' + job.args[1] + '<br>Datetime: ' + str(job.next_run_time) + '<br>'
        st = st + job_s + "<br><br>"
    return st

@application.route('/schedule_text', methods=['POST'])
def schedule_text():
    params = json.loads(request.data)
    phone_number = params["number"]
    msg = params["message"]
    date = params["date"]
    date_to_send = datetime(*date)
    scheduler.add_job(send_reminder, 'date', run_date=date_to_send, args=[msg, phone_number])
    return "Scheduled Text!"

@application.route('/schedule_texts', methods=['POST'])
def schedule_texts():
    email_body = "Text Notifications Scheduled at " + strftime("%Y-%m-%d %H:%M:%S") + "!\n\n"
    checked = False
    messages = json.loads(request.data)
    for message in messages:
        if not checked:
            jobs = scheduler.get_jobs()
            email_body = email_body + "Number: " + str(message["number"]) + "\n\n"
            for job in jobs:
                job_num = ''.join(re.findall('\d+', job.args[1]))
                given_num = ''.join(re.findall('\d+', message["number"])) 
                email_body = email_body + "Removed Job...\n"
                email_body = email_body + "Message: " + job.args[0] + "\n" + "Date: " + str(job.next_run_time) + "\n\n"
                if job_num == given_num:
                    job.remove()
            checked = True
        #print message
        phone_number = message["number"]
        msg = message["message"]
        date = message["date"]
        date_to_send = datetime(*date)
        email_body = email_body + "Added Job...\n"
        email_body = email_body + "Message: " + str(msg) + "\n" + "Date: " + str(date_to_send) + "\n\n"
        scheduler.add_job(send_reminder, 'date', run_date=date_to_send, args=[msg, phone_number])
    sendEmail("Surgery Concierge Log: Texts Scheduled", email_body)
    return "Scheduled all texts! " + str(datetime.now())

def send_reminder(text, number):
    #print "sending message: " + text + " to " + str(number)
    message = client.messages.create(body=text, to="+" + number, from_="+12245889141")


@application.before_first_request
def setup_code():
    scheduler.start()

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    #application.run(port=5001)
    application.run()
   