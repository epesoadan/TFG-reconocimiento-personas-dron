import sys
import os
from flask import Flask, render_template, Response, redirect, url_for
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from log_reader import read_log_file
from stop_program import manage_process
from execute_program import run_execute_program
from controller_info import run_drone_connection_checker
from count_files import count_found_people_pictures

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def read_log():
    log_content = read_log_file()
    return Response(log_content, mimetype='text/plain')

@app.route('/finishProgram', methods=['POST'])
def finish_process():
    message = manage_process()
    return Response(message, mimetype='text/html')

@app.route('/executeProgram')
def run_program():
    run_execute_program()
    return Response("", mimetype='text/html')

@app.route('/checkController')
def check_controller():
    html = run_drone_connection_checker()
    return Response(html, mimetype='text/html')

@app.route('/countPictures', methods=['POST'])
def count_pictures():
    html = count_found_people_pictures()
    return Response(html, mimetype='application/json')

