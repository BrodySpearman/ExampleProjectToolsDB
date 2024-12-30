import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, SmallInteger, text, select
from sqlalchemy.engine import reflection
from sqlalchemy.sql import func
from jinja2 import Template
import mysql.connector


### DATABASE CONNECTION ###

# Delete these variables and encrypt them elsewhere soon.
dbhost = "localhost"
dbuser = "root"
dbpass = "roothost1"
port = "3306"
dbname = "stateline_tools_db"

app = Flask(__name__)

engine = create_engine(
        url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
            dbuser, dbpass, dbhost, port, dbname
        ), echo=True)

conn = engine.connect()
metadata_obj = MetaData(schema='stateline_tools_db')


### TABLE INITIALIZATION ###

avail_databases = ['tool', 'employee', 'checkout']

tool_table = Table(
    "tool",
    metadata_obj,
    autoload_with=engine
)

employee_table = Table(
    "employee",
    metadata_obj,
    autoload_with=engine
)

checkout_table = Table(
    "checkout",
    metadata_obj,
    autoload_with=engine
)


### TABLE FUNCTIONS ###

def get_table_info(tblnme):
    get_table_info.columns = []

    temp_query = f"SELECT * FROM {tblnme}"
    tool_result = conn.execute(text(temp_query))

    for elem in tool_result.cursor.description: 
        get_table_info.columns.append(elem[0]) 

    get_table_info.dataset = tool_result.fetchall()
    print(get_table_info.dataset)
    print(get_table_info.columns)
    

### APP ROUTES ###

# Flask command line operation (Windows):
# set FLASK_APP=app
# set FLASK_ENV=development
# flask run

@app.route('/')
def index():
    get_table_info('tool')
    return render_template('bodycontent.html', get_table_info=get_table_info)


@app.route('/employees')
def employee():
    get_table_info('employee')
    return render_template('bodycontent.html', get_table_info=get_table_info)

