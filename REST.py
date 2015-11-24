from flask import *
from datetime import timedelta
from functools import update_wrapper
import json
import requests
import MySQLdb
import populate

app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/timeline', methods=['POST'])
def timeline():	
	month = request.form['month']
	day = request.form['day']
	year = request.form['year']
	surgery = request.form['surgery']
	query = request.form['query']
#surgerydb 
#
	db = MySQLdb.connect(host="surgeryconcierge.c8wqhnln04ea.us-east-1.rds.amazonaws.com", port=3306,  user="surgery", passwd="concierge",db="insndb")
	cur = db.cursor()
	#SELECT id, surgery_name, month, day, year FROM test_surgeries WHERE patient_id=0;
	cur.execute("SELECT * FROM pennsy_ibc_presurgery;")
	result = cur.fetchall()
	db.close()
	month = int(month)
	day = int(day)
	year = int(year)
	json_result = populate.populate(month, day, year, result, surgery, query)
	return Response(json_result, mimetype='application/json')

@crossdomain(origin="*")
@app.route('/surgery/<patient_id>', methods=['GET'])
def surgery(patient_id):	
	db = MySQLdb.connect(host="surgeryconcierge.c8wqhnln04ea.us-east-1.rds.amazonaws.com", port=3306,  user="surgery", passwd="concierge",db="surgerydb")
	cur = db.cursor()
	#SELECT id, surgery_name, month, day, year FROM test_surgeries WHERE patient_id=0;
	cur.execute("SELECT id, surgery_name, month, day, year FROM test_surgeries WHERE patient_id = " + patient_id+ ";")
	result = cur.fetchall()
	db.close()
	json_result = populate.test_surgeries_to_json(result)
	return Response(json_result, mimetype='application/json')

@app.route('/insns', methods=['GET'])
def insns(surgery_id):	

	db = MySQLdb.connect(host="surgeryconcierge.c8wqhnln04ea.us-east-1.rds.amazonaws.com", port=3306,  user="surgery", passwd="concierge",db="surgerydb")
	cur = db.cursor()
	#SELECT date,conditions, ask_doctor, insn_text FROM test_texttl WHERE patient_id = patient_id
	cur.execute("SELECT date,conditions, ask_doctor, insn_text FROM test_texttl WHERE patient_id = " + surgery_id+ ";")
	result = cur.fetchall()
	db.close()
	json_result = populate.insns_to_json(result)
	return Response(json_result, mimetype='application/json')


if __name__ == '__main__':
	app.run(debug=True)
