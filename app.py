#!flask/bin/python
from flask import request, render_template, Flask
import db, os, spark, sys, json
import requests
app = Flask(__name__)

from random import randint


from ciscosparkapi import CiscoSparkAPI

api = CiscoSparkAPI("ZDY0MThkMDktZDg2Yi00OGYxLWI3MDYtNzljNmEzMGE2ZjBjM2ViOTY1M2YtYTU2")

auth_code = 'Bearer ZDY0MThkMDktZDg2Yi00OGYxLWI3MDYtNzljNmEzMGE2ZjBjM2ViOTY1M2YtYTU2'

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
    addParticipantsToRoom("Y2lzY29zcGFyazovL3VzL1JPT00vZmM2YjFhZjAtODVkNy0xMWU3LWE1NjMtZWI2NzcyYTFmZjVk", "abhiram.304@gmail.com")
    #addParticipantsToRoom(room_id, my_email)
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
    try:
        print("Room id in aPTR ", roomId, " email: ", email_addresses   )
        headers={
        "Content-Type": "application/json; charset=utf-8", 
        "Authorization" : auth_code 
        }
        f = False
        for email in email_addresses:
           url = "https://api.ciscospark.com/v1/memberships"            
           payload = "{\r\n  "+"roomId"+" : "+str(roomId)+",\r\n  "+"personEmail"+": "+str(email)+",\r\n  "+"isModerator"+": "+False+"\r\n}"
           headers = {
            'authorization': "Bearer ZDY0MThkMDktZDg2Yi00OGYxLWI3MDYtNzljNmEzMGE2ZjBjM2ViOTY1M2YtYTU2",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "7658b5dc-3a90-c4cf-9782-781a05d16eb1"
            }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

        print("77777777777777777",r)
    except requests.HTTPError as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", e)


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