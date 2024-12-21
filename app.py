import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, SmallInteger, text, select
from sqlalchemy.engine import reflection
import mysql.connector

from sqlalchemy.sql import func

dbhost = "localhost"
dbuser = "root"
dbpass = "roothost1"
port = "3306"
dbname = "stateline_tools_db"

app = Flask(__name__)

# SqlAlchemy Initialization
engine = create_engine(
        url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
            dbuser, dbpass, dbhost, port, dbname
        ), echo=True)

conn = engine.connect()
metadata_obj = MetaData(schema='stateline_tools_db')

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


temp_query = "SELECT * FROM tool"
tool_result = conn.execute(text(temp_query))
columns = []

for elem in tool_result.cursor.description: 
    columns.append(elem[0]) 

dataset = tool_result.fetchall()

print(dataset)

print(columns)

# Flask command line operation (Windows):
# set FLASK_APP=app
# set FLASK_ENV=development
# flask run

@app.route('/')
def index():
    return render_template('bodycontent.html', dataset=dataset, columns=columns)
    