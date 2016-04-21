''' Homework 10

- Due on Wednesday, April 9 by midnight by online submission through turnin.
- Leave the name of the file unchanged (hw10.py), and submit this file only.
- You *will* be graded on style.
- You may discuss problems with others, but write up the solutions yourself.

This assignment was adapted from a similar one written by Zachary Wasserman,
who taught the minicourse last year.

Your goal will be to create an API for serving basic information about Penn courses.
After consuming Twitter's API in the last homework you should be quite familiar with
JSON, and have a good idea of what an API does.

First you will convert a CSV file containing Registrar data to JSON format. Next, you
will use this data as a source for serving through your API. We leave this open ended,
so please implement helper functions to keep your code DRY (Don't Repeat Yourself). 

'''

from flask import Flask, request, jsonify
import csv
import json
import requests
def csv_to_json(csvfile, jsonfile):
    ''' Load the data in csvfile, convert it to a list of dictionaries,
    and then save the result as JSON to jsonfile.

    The first line of csvfile will include the field names. Each following line
    should be split into its fields and turned into a dictionary. The output should
    be a list of dictionaries, one per line.

    Recall that you did this in previous homework, but you weren't allowed to use the
    DictReader method of the csv module -- now you can. Also, in the previous homework,
    you simply returned the list -- now you should return nothing, but write the result
    in JSON format to the specified file.
    '''
    test_array = []
    with open(csvfile, 'rb') as readin:
        csvreader = csv.DictReader(readin, delimiter=',')
        for row in csvreader:
            test_array.append(row)
    with open(jsonfile, 'wb') as writeout:
        writeout.write(json.dumps(test_array))

def load_json(jsonfile):
    ''' Load JSON data from the given filename. Note that this should return Python
    data structures, not a string of JSON. If jsonfile does not contain valid JSON,
    raise an exception.
    '''
    try:
        with open(jsonfile) as data_file:
            return json.load(data_file)
    except ValueError:
        raise InvalidJsonException()

        


''' Convert courses.csv to courses.json. Uncomment when you have defined csv_to_json. '''
csv_to_json('courses.csv', 'courses.json')
    
''' Load the course data into a global variable, which should be used by your Flask
application. Uncomment this when you have defined load_json.'''
COURSES = load_json('courses.json')

app = Flask(__name__)

def helper(dept,code=None,section=None):
    department = []
    codenum = []
    sectionnum = []
    dic = {}
    for course in COURSES:
        if section and course['section'] == section and course['code'] == code and course['dept'] == dept:
            holder = section.split("?type=")
            if (len(holder) == 2) and course['type'] == holder[1]:
                sectionnum.append(course)
            elif len(holder) == 1:
                sectionnum.append(course)
        elif code and (not section) and course['code'] == code and course['dept'] == dept:
            holder = code.split("?type=")
            if (len(holder) == 2) and course['type'] == holder[1]:
                codenum.append(course)
            elif len(holder) == 1:
                codenum.append(course)
        elif (dept and course['dept'] == dept and (not code) and (not section)):
            holder = dept.split("?type=")
            if (len(holder) == 2) and course['type'] == holder[1]:
                department.append(course)
            elif len(holder) == 1:
                department.append(course)
    if section:
        return sectionnum
    elif code:
        return codenum
    elif dept:
        return department
    else:
        return COURSES


@app.route('/courses/<dept>')
@app.route('/courses/<dept>/<code>')
@app.route('/courses/<dept>/<code>/<section>')
def courses(dept, code=None, section=None):
    ''' Returns a list of courses matching the query parameters.

    The response should be JSON of the following format:
    { "results": [list of courses] }
    Each course in the list should be represented by a dictionary.

    Note that JSON should never have lists at the top level due to security issues with
    Javascript. See http://flask.pocoo.org/docs/security/#json-security for more.
    That's why we return a dictionary with one key/value pair instead.

    For any parameters not provided, match any value for that parameter. For instance,
    accessing /courses/cis should return a list of all CIS courses, and accessing
    courcies/cis/110 should return a list of all sections for CIS 110.

    There is also an optional GET request parameter for the 'type' key found in the CSV file.
    You should detect that and use it if it is provided. For instance, accessing /courses/cis?type=REC
    should return a list of all CIS recitation sections.

    Example: accessing the endpoint /courses/cis/110/001 should return the following JSON:
    
    {
      "results": [
        {
          "code": "110",
          "dept": "CIS",
          "instructor": "BROWN B",
          "name": "Intro To Comp Prog               ",
          "section": "001",
          "type": "LEC"
          ...
        }
      ]
    }
    '''
    return jsonify(results=helper(dept,code,section))


@app.route('/schedule', methods=['POST'])
def schedule():
    ''' A POST-only endpoint. Accept POST data of the form:
    {'courses': [ list of courses ]}
    
    Each course dictionary in the list should have 'dept', 'code', and 'section' keys.
    Look up each course and find its meeting times. (If the given dictionary does
    not match any course, just skip it.) Construct and return a corresponding JSON
    schedule, where keys are the days of the week, and values are a list of courses
    that meet on that day. See the following example for details.

    Suppose the list of courses is:
    [{'dept': 'ACCT', 'code': '297', 'section': '402'},
     {'dept': 'MATH', 'code': '104', 'section': '226'},
     {'dept': 'CIS', 'code': '521', 'section': '001'}]

    Note that when someone sends this data, they need to JSON-encode it, i.e. turn the list
    into a string that can be sent over HTTP. So a request to this endpoint will look like:
    req = requests.post(.., data={'courses': json.dumps(list_of_courses)})

    Then req.json() should equal:
    {
        u'Monday':    [u'Taxes And Bus Strategy: 12-1:30PM'],
        u'Tuesday':   [u'Fundamentals Of Ai: 10:30-12NOON'],
        u'Wednesday': [u'Calculus I: 9-10AM', u'Taxes And Bus Strategy: 12-1:30PM']
        u'Thursday':  [u'Fundamentals Of Ai: 10:30-12NOON'],
    }

    Some notes: 1. Remember that dictionaries are unordered data structures, so the order
    of keys does not matter; 2. The class lists should be in alphabetical order of class
    name; 3. if there is no class on a particular day, don't include a key for that day.
    '''
    #initialize lists for each weekday
    m = []
    t = []
    w = []
    r = []
    f = []
    schedule = {}
    courselist = []
    #returns list of class dictionaries
    Courses = json.loads(request.form['courses'])
    for course in Courses:
        #combine current dict with next dictionary
        courselist = courselist + helper(course['dept'], course['code'], course['section'])
    #parse through all courses
    for course in courselist:
        times = course["times"].split(" ")
        if (times[0] != "TBA"):
            for day in times[0]:
                if day == "M":
                    m.append(course['name'].rstrip() + ": " + times[1])
                elif day == "T":
                    t.append(course['name'].rstrip() + ": " + times[1])
                elif day == "W":
                    w.append(course['name'].rstrip() + ": " + times[1])
                elif day == "R":
                    r.append(course['name'].rstrip() + ": " + times[1])
                elif day == "F":
                    f.append(course['name'].rstrip() + ": " + times[1])
    if m:
        schedule['Monday'] = sorted(m)
    if t:
        schedule['Tuesday'] = sorted(t)
    if w:
        schedule['Wednesday'] = sorted(w)
    if r:
        schedule['Thursday'] = sorted(r)
    if f:
        schedule['Friday'] = sorted(f)
    return jsonify(schedule)



        
    
if __name__ == '__main__':
    app.run()
