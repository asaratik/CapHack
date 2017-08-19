from app import app
from flask import request, render_template
import sys

@app.route('/')
def index():
    return  "hello"
