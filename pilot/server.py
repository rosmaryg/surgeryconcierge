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
  subprocess.call(["python", "new_calendar.py", "--data", "\"" + str(request.args) + "\""])
  return 'Calendar succesfully created! You may now close this window.'

if __name__ == '__main__':
  app.run(debug=True)
