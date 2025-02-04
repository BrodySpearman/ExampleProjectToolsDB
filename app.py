import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

import pymysql.cursors
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, text, select
from sqlalchemy.engine import reflection
from sqlalchemy.sql import func
from jinja2 import Template
from flaskext.mysql import MySQL
import pymysql
import json

# Flask command line operation (Windows):
# set FLASK_APP=app
# set FLASK_ENV=development
# flask run

### DATABASE CONNECTION ###
# Delete these variables, change and encrypt them elsewhere soon.

dbhost = "localhost"
dbuser = "root"
dbpass = "roothost1"
port = "3306"
dbname = "stateline_tools_db"

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = dbuser
app.config['MYSQL_DATABASE_PASSWORD'] = dbpass
app.config['MYSQL_DATABASE_DB'] = dbname
app.config['MYSQL_DATABASE_HOST'] = dbhost
mysql.init_app(app)

engine = create_engine(
        url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
            dbuser, dbpass, dbhost, port, dbname
        ), echo=True)

metadata_obj = MetaData(schema='stateline_tools_db')

### TABLE INITIALIZATION ###

avail_tables = ['tool', 'employee', 'checkout']

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

data = []

# Get the column names of a table (tblnme). 
def get_col_names(tblnme):
    conn = engine.connect()
    columns = []

    temp_query = f"SELECT * FROM {tblnme} LIMIT 1"
    tool_result = conn.execute(text(temp_query))

    for elem in tool_result.cursor.description: 
        columns.append(elem[0]) 

    conn.close()
    return columns

def get_table_data(tblenme):
    conn = engine.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    data = []

    cursor.execute(f"SELECT * FROM {tblenme}")
    datalist = cursor.fetchall()
    tblclms = get_col_names(tblenme)

    for row in datalist:
        data.append({
            tblclms[0]: row[tblclms[0]],
            tblclms[1]: row[tblclms[1]],
            tblclms[2]: row[tblclms[2]],
            tblclms[3]: row[tblclms[3]],
            tblclms[4]: row[tblclms[4]],
            tblclms[5]: row[tblclms[5]],
            tblclms[6]: row[tblclms[6]]
        })
    
    return data
    
    

### APP ROUTES ###

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('base.html')

@app.route('/tools', methods = ['GET', 'POST'])
def tool_table_show():
    tool_table_cols = get_col_names('tool')
    return render_template('tool_table.html', tool_table_cols=tool_table_cols)

@app.route('/ajaxtools', methods = ['GET', 'POST'])
def ajaxtools():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw']
            print(draw)

            cursor.execute("SELECT * FROM tool")
            tool_list = cursor.fetchall()

            data = []
            for row in tool_list:
                data.append({
                    'ToolID': row['ToolID'],
                    'Type': row['Type'],
                    'ToolName': row['ToolName'],
                    'Brand': row['Brand'],
                    'SKU': row['SKU'],
                    'SerialNum': row['SerialNum'],
                    'Description': row['Description']
                })
            
            response = {
                'draw': draw,
                'iTotalRecords': 20,
                'iTotalDisplayRecords': 20,
                'aaData': data
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/create_new_tool', methods = ['GET', 'POST'])
def get_tool_data():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            pass
            # the client side will send a form with the html parameter 'action' (string) and 'data' (object).
            # the 'action' parameter will determine what the server will do with the data (create). "action  = create"
            # the 'data' parameter will contain the data object, with data to be inserted into the database.  "data[0][column]  = data_val"
            # The server will update the database with the new row and return the new row's data to the client.
            # the response will be an object containing the new row's data.
            # an example of the data object is as follows: "data": [{"Type": "Hand Tool", "ToolName": "Hammer", "Brand": "Stanley", "SKU": "STAN-123", "SerialNum": "123456", "Description": "A hammer"}]
            # after the the response is sent back to the client, the client will update the table with the new row.

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/checkouts', methods = ['GET', 'POST'])
def checkout_table_show():

    checkout_table_cols = get_col_names('checkout')
    return render_template('checkout_table.html', checkout_table_cols=checkout_table_cols)

@app.route('/employees', methods = ['GET', 'POST'])
def employee_table_show():

    employee_table_cols = get_col_names('employee')
    return render_template('employee_table.html', checkout_table_cols=employee_table_cols)

if __name__ == '__main__':
    app.run(debug=True)
