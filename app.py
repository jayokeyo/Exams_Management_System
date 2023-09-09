#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, redirect, jsonify, make_response, render_template, url_for, request, flash
from flask_cors import CORS, cross_origin
from flasgger import Swagger
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy import create_engine, insert
import os
import pandas as pd
from werkzeug.exceptions import HTTPException
from models import *
from models import storage
from models.result import Result
from distutils.log import debug
from fileinput import filename
from os.path import join, dirname, realpath
import console


app = Flask(__name__)
swagger = Swagger(app)
app.url_map.strict_slashes = False
host = os.getenv('EMS_API_HOST', '0.0.0.0')
port = os.getenv('EMS_API_PORT', 5000)
#cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
#app.register_blueprint(app_views)

global teacher_id
global dash_obj
global name
name = "EMS USER"
teacher_id = ""
dash_obj = {}
path = os.getcwd()
app.secret_key = 'd3aaad1cd5790d3539c83760df66138d594a833e4b656270320a92317266fe67'
UPLOAD_FOLDER = join(path, 'uploads')
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
conn = create_engine('mysql+mysqldb://root@localhost/EMS_dev', pool_pre_ping=True).connect()

@app.route('/', methods = ["GET"], strict_slashes=False)
def login_page():
    '''Render login page'''
    return render_template('login.html')

@app.route('/', methods = ["POST"], strict_slashes=False)
def login():
    global teacher_id
    global name
    '''Authentication method'''
    email = request.form.get('email')
    password = request.form.get('password')
    all_teachers = storage.all("Teacher").values()
    for teacher in all_teachers:
        if (teacher.email == email and teacher.password == password):
            teacher_id = teacher.id
            name = teacher.first_name+" "+teacher.surname
            return redirect(url_for('home', name = name, teacher_id = teacher_id))
    flash('Please check your login details and try again.')
    return redirect(url_for('login'))

@app.route('/<teacher_id>/home', methods = ["GET", "POST"], strict_slashes=False)
def home(teacher_id):
    """homeview for a specific teacher"""
    try:
        dashboards = dash_obj[teacher_id]
    except KeyError:
        return render_template('welcome.html')
    else:
        return render_template("home.html", dashboards = dashboards)

@app.route('/createdashboard', methods = ['GET'], strict_slashes=False)
def CreateDashboard_post():
    '''page for inserting dashboard details'''
    return render_template('createdashboard.html')

@app.route('/createdashboard', methods = ['POST'], strict_slashes=False)
def CreateDashboard():
    """logic for creating new dashboard"""
    global dash_obj
    newDashboard = {"name": request.form.get('name'), "description": request.form.get('description')}
    try:
        dash_obj[teacher_id].append(newDashboard)
        print(dash_obj[teacher_id])
    except KeyError:
        dash_obj[teacher_id] = [newDashboard,]
        print(dash_obj[teacher_id])
    return redirect(url_for('home', teacher_id = teacher_id))

@app.route('/dashboards/<name>', methods = ['GET', 'POST'], strict_slashes=False)
def Dashboard(name):
    """view for a specific dashboards"""
    return render_template("dashboard.html")

@app.route('/<dashboard_id>/addgraph', methods = ["GET", "POST"], strict_slashes=False)
def AddGraph(dashboard_id):
    """logic for adding a graph to dashboard"""
    query = "SELECT "
    query+request.form["COLUMN1"]
    if (request.form["column2"] != NULL):
        query+", "+request.form["COLUMN2"]+" "
    query+"FROM results WHERE "+request.form["WHERE"]+" "
    if (request.form["GROUPBY"] != NULL):
        query+"GROUPBY "+request.form["GROUPBY"]
    df = pd.read_sql(query, 'mysql:///EMS_dev')

    if (request.form["column2"] != NULL):
        dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": df[request.form["column1"]],
                            "y": df[request.form["column2"]],
                            "type": "lines",
                        },
                    ],
                    "layout": {"title": request.form["description"]}, #Add description to form
                },
            )
    else:
        dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": df["GROUPBY"],
                            "y": df["COLUMN1"],
                            "type": "lines",
                        },
                    ],
                    "layout": {"title": request.form["description"]},
                },
            )

@app.route('/uploadcsv', strict_slashes=False)
def UploadCSV_form():
    '''render form for file upload'''
    return render_template('upload_csv.html')

@app.route('/uploadcsv', methods = ["POST"], strict_slashes=False)
def UploadCSV():
    #add a routine cleanup function
    if request.method == 'POST':
        f = request.files['file']
        path_to_file = join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(join(path_to_file))
        col_names = ['exam_id','subject_id','student_id', 'class_id', 'score' , 'grade']
        df = pd.read_csv(path_to_file, names=col_names, header=None)
        df = df.reset_index() 
        for i,row in df.iterrows():
            if (i == 0):
                continue
            newResult = Result()
            newResult.exam_id = row['exam_id']
            newResult.subject_id = row['subject_id']
            newResult.student_id = row['student_id']
            newResult.class_id = row['class_id']
            newResult.score = row['score']
            newResult.grade = row['grade']
            storage.new(newResult)
            storage.save()
        flash('File successfully uploaded')
    return redirect(url_for('home', teacher_id = teacher_id))

@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
