from app import app
from flask import request, render_template
import db
import spark
import sys

@app.route('/')
def index():
    return  "hello"

@app.route('/list_rooms')
def list_rooms():
	return spark.list_rooms('CAPHACK')