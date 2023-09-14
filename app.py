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
teacher_id = ""
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
    '''Authentication method'''
    email = request.form.get('email')
    password = request.form.get('password')
    all_teachers = storage.all("Teacher").values()
    for teacher in all_teachers:
        if (teacher.email == email and teacher.password == password):
            teacher_id = teacher.id
            name = teacher.first_name+" "+teacher.surname
            return redirect(url_for('home', teacher_id = teacher_id))
    return redirect(url_for('login'))

@app.route('/<teacher_id>/home', methods = ["GET", "POST"], strict_slashes=False)
def home(teacher_id):
    """homeview for a specific teacher"""
    all_dashboards = storage.all("Dashboards").values()
    for dashboard in all_dashboards:
        if (dashboard.teacher_id != teacher_id):
            del(dashboard)
    if (len(all_dashboards) == 0):
        return render_template('welcome.html')
    return render_template("home.html", dashboards = all_dashboards)

@app.route('/createdashboard', methods = ['GET'], strict_slashes=False)
def CreateDashboard_post():
    '''page for inserting dashboard details'''
    return render_template('createdashboard.html')

@app.route('/createdashboard', methods = ['POST'], strict_slashes=False)
def CreateDashboard():
    """logic for creating new dashboard"""
    newDashboard = Dashboard()
    newDashboard.name = request.form.get('name')
    newDashboard.description = request.form.get('description')
    teacher_id = teacher_id
    return redirect(url_for('home', teacher_id = teacher_id))

@app.route('/dashboards/<dashboard_id>', methods = ['GET'], strict_slashes=False)
def Dashboard(dashboard_id):
    """view for a specific dashboards"""
    all_graphs = storage.all("Graphs").values()
    for graph in all_graphs:
        if (graph.dashboard_id != dashboard_id):
            del(graph)
    if (len(all_graphs != 0)):
        app.layout = html.Div(
                children=[
                    html.H1(children=dashboard.name),
                    html.P(children=(dashboard.description),),
                    for graph in all_graphs:
                        if (graph.y_axis != NULL):
                            dcc.Graph(
                                figure={
                                    "data": [
                                        {
                                            "x": graph.x_axis,
                                            "y": graph.y_axis,
                                            "type": graph.graph_type,
                                            },
                                        ],
                                    "layout": {"title": graph.description},
                                    },
                                ),
                        else:
                            dcc.Graph(
                                figure={
                                    "data": [
                                        {
                                            "x": graph.group_by,
                                            "y": graph.x_axis,
                                            "type": graph.graph_type,
                                            },
                                        ],
                                    "layout": {"title": graph.description},
                                    },
                                ),
                            html.a(children='Add Graph', href=graph.dashboard_id+'/addgraph',target='_blank')
                            ]
                )

@app.route('/<dashboard_id>/addgraph', methods = ["GET"], strict_slashes=False)
def AddGraph_post(dashboard_id):
    """form for adding a graph"""
    return render_template('addgraph.html')

@app.route('/<dashboard_id>/addgraph', methods = ["POST"], strict_slashes=False)
def AddGraph(dashboard_id):
    """logic for adding a graph to dashboard"""
    if (request.method == "POST"):
        newGraph = Graph()
        newGraph.dashboard_id = dashboard_id
        newGraph.x_axis = request.form.get("x_axis")
        newGraph.y_axis = request.form.get("y_axis")
        newGraph.condition = request.form.get("condition")
        newGraph.condition = request.form.get("condition")

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
