import subprocess
from flask import request
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/dashboard.html')
def calendar():
  return render_template('dashboard.html')

@app.route('/generate-calendar')
def genCalendar():
  ret_val = subprocess.call(["python", "new_calendar.py", "--data", "\"" + str(request.args) + "\""])
  if ret_val == 0:
    return 'Calendar succesfully created! You may now close this window. <br> <a href="http://google.com/calendar">View my calendar<a>'
  else:
    return 'Calendar not created.'

if __name__ == '__main__':
  app.run(debug=True)
