#!flask/bin/python
from flask import request, render_template, Flask
import db, os, spark, sys, json

app = Flask(__name__)

from random import randint


from ciscosparkapi import CiscoSparkAPI

api = CiscoSparkAPI("ZDY0MThkMDktZDg2Yi00OGYxLWI3MDYtNzljNmEzMGE2ZjBjM2ViOTY1M2YtYTU2")

global room_id
@app.route('/')
def index():
    return  "hello"

@app.route('/worker', methods=['POST'])
def worker_serve():
    body = json.loads(request.data)
    print("-----------------------------", body)
    q = body['result']['resolvedQuery']
    query = q.encode('ascii','ignore')
    event = query.split(" ")
    print "Speech in Server ----------------------------......... ", query
    res =    {
    "speech": "Hello i've sent the request",
    "displayText": "Barack Hussein Obama II was the 44th and current President of the United States, and the first African American to hold the office. Born in Honolulu, Hawaii, Obama is a graduate of Columbia University   and Harvard Law School, where ",
    "data":{},
    "contextOut": [],
    "source": "DuckDuckGo"
    }
    my_email  = body['originalRequest']['data']['data']['personEmail'].encode('ascii','ignore')
    print("::::::::USER EMAIL::::::::::",my_email)
    my_message = ("One of your colleague dashed for ")+str(event[1])+(". If interested ding them replying here saying DING")
    post_message(my_message, 1, event[1])
    room_name = str(event[1]) + str(randint(0, 99))
    room_id = create_room(room_name).encode('ascii','ignore')
    print(":::::::::::::::ROOM ID::::::::;;;;;", room_id)
    email_arr =[]
    email_arr.append(my_email)
    addParticipantsToRoom(room_id, my_email)
    return json.dumps(res), 201
#send a message to same random(contacts) 

@app.route('/workerDing', methods=['POST'])
def worker_serve_ding():
    body = json.loads(request.data)
    print("-----------------------------", body)
    email = body
    res =    {
    "speech": "Thanks for your interest. You will be added to a spark chat room.",
    "displayText": "Thanks for your interest. You will be added to a spark chat room",
    "data":{},
    "contextOut": [],
    "source": "DuckDuckGo"
    }
    my_email  = "abhiram.304@gmail.com"



def post_message(message, noOfPeople, senderEmail):
	emailList = ['marupati.udaykiran@gmail.com']
	for x in range(0, noOfPeople):
		if emailList[x] != senderEmail:
			api.messages.create(toPersonEmail=emailList[x], text=message)

def createMessage(toEmail, message):
	api.messages.create(toPersonEmail=toEmail, text=message)


def create_room(roomName):
    return api.rooms.create(roomName).id

def addParticipantsToRoom(roomId, email_addresses):
    for email in email_addresses:
        api.memberships.create(roomId, personEmail=email)



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