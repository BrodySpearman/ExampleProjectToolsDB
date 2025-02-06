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

# Retrieve data from db and draw table on the client side.
def draw_table(tblenme):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw']
            print(draw)

            cursor.execute(f"SELECT * FROM {tblenme}")
            datalist = cursor.fetchall()
            tblclms = get_col_names(tblenme)

            data = []

            if tblenme == 'tool':
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
    return draw_table('tool')

@app.route('/create_new_tool', methods = ['GET', 'POST'])
def create_new_tool():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':

            # Client form example (ImmutableMultiDict):
            # ([('data[0][Type]', 'value'), ('data[0][ToolName]', 'value'), ('data[0][Brand]', 'value'), ('data[0][SKU]', 'value'), ('data[0][SerialNum]', 'value'), ('data[0][Description]', 'value'), ('action', 'create')])
            data = request.form.to_dict(flat=False)
            print(data)

            cursor.execute(f"""INSERT INTO tool (ToolID, Type, ToolName, Brand, SKU, SerialNum, Description) 
                            VALUES 
                            ({data['data[0][ToolID]']},
                            '{data['data[0][Type]']}',
                            '{data['data[0][ToolName]']}',
                            '{data['data[0][Brand]']}',
                            '{data['data[0][SKU]']}',
                            '{data['data[0][SerialNum]']}',
                            '{data['data[0][Description]']}')""")
            conn.commit()
            
            new_data = {
                'ToolID': data['data[0][ToolID]'],
                'Type': data['data[0][Type]'],
                'ToolName': data['data[0][ToolName]'],
                'Brand': data['data[0][Brand]'],
                'SKU': data['data[0][SKU]'],
                'SerialNum': data['data[0][SerialNum]'],
                'Description': data['data[0][Description]']
            }

            response = {
                'data': new_data
            }

            return jsonify(response)

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
