from flask import *
import json
import requests
import MySQLdb
import populate

app = Flask(__name__)

@app.route('/surgery/<month>/<day>/<year>/<surgery>/<query>')
def surgery(month, day, year, surgery, query):	
	db = MySQLdb.connect(host="surgeryconcierge.c8wqhnln04ea.us-east-1.rds.amazonaws.com", port=3306,  user="surgery", passwd="concierge",db="insndb")
	cur = db.cursor()
	cur.execute("SELECT * FROM pennsy_ibc_presurgery")
	result = cur.fetchall()
	db.close()
	month = int(month)
	day = int(day)
	year = int(year)
	json_result = populate.populate(month, day, year, result, surgery, query)
	return Response(json_result, mimetype='application/json')
if __name__ == '__main__':
	app.run(debug=True)
