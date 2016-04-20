import subprocess
import requests
import json
from flask import request
from flask import Flask, render_template, make_response

application = Flask(__name__)

@application.route('/')
def index():
  return render_template('index.html')

# @application.route('/new-template/', methods=['POST'])
# def newTemplate():
#   print "CREATE"
#   json=request.form['data']
#   ret_val = subprocess.call(["python", "new_template.py", json])
#   if ret_val == 0:
#     return 'New template successfully added.'
#   else:
#     return 'Error: New template not added.'

if __name__ == '__main__':
  application.debug = True
  application.run()
