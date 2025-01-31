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

# Old function to collect table data and column names. Needed to generate table data, but planning on phasing out. 
def get_table_info(tblnme):
    conn = engine.connect()
    get_table_info.columns = []

    temp_query = f"SELECT * FROM {tblnme}"
    tool_result = conn.execute(text(temp_query))

    for elem in tool_result.cursor.description: 
        get_table_info.columns.append(elem[0]) 

    get_table_info.dataset = tool_result.fetchall()
    print(get_table_info.dataset)
    print(get_table_info.columns)
    conn.close()


### APP ROUTES ###

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('base.html')

@app.route('/tools', methods = ['GET', 'POST'])
def tool_table_show():
    get_table_info('tool')
    return render_template('tool_table.html', get_table_info=get_table_info)

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

@app.route('/tooladder', methods = ['POST'])
def tooladder():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            data = request.get_json()

            tool_id = data['ToolID']
            tool_type = data['Type']
            tool_name = data['ToolName']
            brand = data['Brand']
            sku = data['SKU']
            serial_num = data['SerialNum']
            description = data['Description']

            cursor.execute("INSERT INTO tool (ToolID, Type, ToolName, Brand, SKU, SerialNum, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (tool_id, tool_type, tool_name, brand, sku, serial_num, description))
            conn.commit()

            response = {
            'data': {
                'ToolID': tool_id,
                'Type': tool_type,
                'ToolName': tool_name,
                'Brand': brand,
                'SKU': sku,
                'SerialNum': serial_num,
                'Description': description
            }
        }
        return jsonify(response)  
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/checkouts', methods = ['GET', 'POST'])
def checkout_table_show():

    get_table_info('checkout')
    return render_template('checkout_table.html', get_table_info=get_table_info)

@app.route('/employees', methods = ['GET', 'POST'])
def employee_table_show():

    get_table_info('employee')
    return render_template('employee_table.html', get_table_info=get_table_info)

if __name__ == '__main__':
    app.run(debug=True)
