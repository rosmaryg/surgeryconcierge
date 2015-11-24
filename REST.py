from flask import *
import json
import requests
import MySQLdb
import populate

app = Flask(__name__)


#Once they open page, call this method
#lists their surgeries (pulling from test_surgeries)
#pull surgery name field from table, store id, & month, day, year etc

#add a surgery_id field in the html to the table 
#In table: See aech surgery' name, month, day, year 

#export surgeryname pdf button next to each row

#get_pdf will take whatever populate puts out -> 
#
#connect to test_texttl table ~> 
# SELECT month, day, year, days_before, conditions, ask_doctor, insn_text FROM 
# test_texttl WHERE surgery_id=id
#New json function takes in surgery name, surgery month, surgery day, surgery year, list of steps (date, conditions, ask_doctor, insn_text) [text_tl stuff]
#
#resulting json -> get pdf python call





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

@app.route('/surgery', methods=['GET'])
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

	db = MySQLdb.connect(host="surgeryconcierge.c8wqhnln04ea.us-east-1.rds.amazonaws.com", port=3306,  user="surgery", passwd="concierge",db="INSERT_DB_NAME_HERE")
	cur = db.cursor()
	#SELECT id, surgery_name, month, day, year FROM test_surgeries WHERE patient_id=0;
	cur.execute("SELECT date,conditions, ask_doctor, insn_text FROM test_texttl WHERE patient_id = " + surgery_id+ ";")
	result = cur.fetchall()
	db.close()
	json_result = populate.insns_to_json(result)
	return Response(json_result, mimetype='application/json')


if __name__ == '__main__':
	app.run(debug=True)
