from app import app
from flask import request, render_template
import db
import spark
import sys
import json

@app.route('/')
def index():
    return  "hello"

@app.route('/list_rooms/<keyword>')
def list_rooms(keyword):
	roomdata = ', '.join([str(room) for room in spark.list_rooms(keyword)])
	return "<h1>"+roomdata+"</h1>"

@app.route('/web_hook', methods=['POST'])
def web_hook():
	body = json.loads(request.data)
	return body