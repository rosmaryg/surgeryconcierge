from flask import Flask
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import TwilioRestClient
from datetime import datetime


application = Flask(__name__)
scheduler = BackgroundScheduler()

#account_sid = "SK2a72b2e69a384838e82640aa07c2fa3a"
#auth_token = "kRdEtj8xQg1wA4JOc80ZPPN0ddetB743"
account_sid = "AC993d85892ae868d46074d1629efa2dc2"
auth_token = "7ebc350c70162239eaf85bd2a4a56b70"
client = TwilioRestClient(account_sid, auth_token)

@application.route('/')
def homepage():
    return "Notifications Node Homepage."

@application.route('/schedule_text', methods=['POST', 'GET'])
def schedule_text():
    if request.method == 'GET':
        phone_number = request.args.get("number")
        msg = request.args.get("message")
        time = request.args.get("time")
    elif request.method == 'POST':
        phone_number = request.form["number"]
        msg = request.form["message"]
        time = request.form["time"]
    return "Scheduled Text!"

@application.route('/schedule_texts', methods=['POST', 'GET'])
def schedule_texts():
    params = request.form
    return "PARAMS (JSON) RECEIVED: " + params

def send_reminder(text, number):
    print "sending message: " + text + " to " + str(number)
    message = client.messages.create(body=text, to="+" + number, from_="+12245889141")

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    scheduler.add_job(send_reminder, 'date', run_date=datetime.now(), args=['TEST MSG2', '14842229088'])
    scheduler.start()
    print 'about to run app'
    application.run()
   