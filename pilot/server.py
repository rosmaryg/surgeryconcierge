import subprocess
from flask import request
from flask import Flask, render_template, make_response

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
    return 'Calendar succesfully created!   <a href="http://google.com/calendar">View my calendar</a> <br><br> <button onClick=\"window.close()\"">Close window</button>'
  else:
    return 'Calendar not created.'

@app.route('/generate-pdf')
def genPdf():
  pdf = subprocess.check_output(["python", "new_pdf.py", "--data", "\"" + str(request.args) + "\""])
  print "before pdf"
  print "pdf " + pdf
  print "after pdf"
  response = make_response(pdf)
  response.headers['Content-Disposition'] = "inline; filename='Instructions.pdf"
  response.mimetype = 'application/pdf'
  return response
  # ret_val = subprocess.call(["python", "new_calendar.py", "--data", "\"" + str(request.args) + "\""])
  # if ret_val == 0:
  #   return 'Calendar succesfully created! You may now close this window. <br> <a href="http://google.com/calendar">View my calendar<a>'
  # else:
  #   return 'Calendar not created.'

if __name__ == '__main__':
  app.run(debug=True)
