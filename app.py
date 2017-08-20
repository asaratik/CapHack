#!flask/bin/python
from flask import request, render_template, Flask
import db, os, spark, sys, json

app = Flask(__name__)

@app.route('/')
def index():
    return  "hello"

@app.route('/worker', methods=['POST'])
def worker_serve():
    res =    {
    "speech": "Hemu swamy. Rasik rajaa",
    "displayText": "Barack Hussein Obama II was the 44th and current President of the United States, and the first African American to hold the office. Born in Honolulu, Hawaii, Obama is a graduate of Columbia University   and Harvard Law School, where ",
    "data":{},
    "contextOut": [],
    "source": "DuckDuckGo"
    }
    return json.dumps(res), 201

@app.route('/list_rooms/<keyword>')
def list_rooms(keyword):
	roomdata = ', '.join([str(room) for room in spark.list_rooms(keyword)])
	return "<h1>"+roomdata+"</h1>"

@app.route('/web_hook', methods=['POST'])
def web_hook():
	body = json.loads(request.data)
	return json.dumps(body)

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	#app.run(debug=True)