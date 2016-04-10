import subprocess
import requests
import json
from flask import request
from flask import Flask, render_template, make_response

application = Flask(__name__)

@application.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  application.debug = True
  application.run()
