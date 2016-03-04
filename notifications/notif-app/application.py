from flask import Flask
from flask import request


application = Flask(__name__)

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
    return "Scheduled Texts!"


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()