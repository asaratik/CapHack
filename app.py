#!flask/bin/python
from flask import request, render_template, Flask
import db, os, spark, sys, json

app = Flask(__name__)

from ciscosparkapi import CiscoSparkAPI

api = CiscoSparkAPI("ZDY0MThkMDktZDg2Yi00OGYxLWI3MDYtNzljNmEzMGE2ZjBjM2ViOTY1M2YtYTU2")


@app.route('/')
def index():
    return  "hello"

@app.route('/worker', methods=['POST'])
def worker_serve():
    res =    {
    "speech": "Hello i've sent the request",
    "displayText": "Barack Hussein Obama II was the 44th and current President of the United States, and the first African American to hold the office. Born in Honolulu, Hawaii, Obama is a graduate of Columbia University   and Harvard Law School, where ",
    "data":{},
    "contextOut": [],
    "source": "DuckDuckGo"
    }
    my_email  = "abhiram.304@gmail.com"
    my_message = "cricket"
    post_message(my_message, 1, my_email)
    return json.dumps(res), 201
#send a message to same random(contacts) 

def post_message(message, noOfPeople, senderEmail):
	emailList = ['ashokaratikatla@gmail.com', 'marupati.udaykiran@gmail.com']
	for x in range(0, noOfPeople-1):
		if emailList[x] != senderEmail:
			api.messages.create(toPersonEmail=emailList[x], text=message)

def createMessage(toEmail, message):
	api.messages.create(toPersonEmail=toEmail, text=message)



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