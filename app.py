import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String
from sqlalchemy.engine import reflection
import mysql.connector

from sqlalchemy.sql import func

dbhost = "localhost"
dbuser = "root"
dbpass = "roothost1"
port = "3306"
dbname = "stateline_tools_db"

# Database link string builder
mydb = mysql.connector.connect(
    host = dbhost,
    user = dbuser,
    password = dbpass,
    database = dbname
)

# SqlAlchemy Initialization
engine = create_engine(
        url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
            dbuser, dbpass, dbhost, port, dbname
        ), echo=True)

insp = reflection.Inspector.from_engine(engine)
for table in insp.get_table_names():
    print(insp.get_columns(table))

print(mydb)

# Flask command line operation (Windows):
# set FLASK_APP=app
# set FLASK_ENV=development
# flask run

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('bodycontent.html')
    