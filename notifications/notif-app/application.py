from flask import Flask
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import TwilioRestClient
from datetime import datetime
from datetime import timedelta
import json


application = Flask(__name__)
scheduler = BackgroundScheduler()
templist = []

#account_sid = "SK2a72b2e69a384838e82640aa07c2fa3a"
#auth_token = "kRdEtj8xQg1wA4JOc80ZPPN0ddetB743"
account_sid = "AC993d85892ae868d46074d1629efa2dc2"
auth_token = "7ebc350c70162239eaf85bd2a4a56b70"
client = TwilioRestClient(account_sid, auth_token)

@application.route('/')
def homepage():
    return "Notifications Node Homepage."

@application.route('/view_jobs', methods=['GET'])
def view_jobs():
    jobs = scheduler.get_jobs()
    st = ''
    for job in jobs:
        st = st + ' | ' + job.name + ', ' + str(job.func) + ', ' + str(job.args)
    return st + "<br><br>" + str(templist)

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
    messages = json.loads(request.data)
    for message in messages:
        phone_number = params["number"]
        msg = params["message"]
        date = params["date"]
        date_to_send = datetime(*date)
        scheduler.add_job(send_reminder, 'date', run_date=date_to_send, args=[msg, phone_number])
    return "Scheduled all texts!"

def send_reminder(text, number):
    print "sending message: " + text + " to " + str(number)
    message = client.messages.create(body=text, to="+" + number, from_="+12245889141")


@application.before_first_request
def setup_code():
    scheduler.start()

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
   