from config import Config
from __init__ import mysql
from flask import request, jsonify
from sqlalchemy import create_engine, MetaData, Table, text
import pymysql.cursors

engine = create_engine(
    url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
        Config.dbuser, Config.dbpass, Config.dbhost, Config.port, Config.dbname
    ), echo=True)

avail_tables = ['tool', 'employee', 'checkout']
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

checkout_table = Table(
    "checkout",
    metadata_obj,
    autoload_with=engine
)

def init_db(app):
    mysql.init_app(app)


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
            
            if tblenme == 'employee':
                for row in datalist:
                    data.append({
                        tblclms[0]: row[tblclms[0]],
                        tblclms[1]: row[tblclms[1]],
                        tblclms[2]: row[tblclms[2]]
                    })

            if tblenme == 'checkout':
                for row in datalist:
                    data.append({
                        tblclms[0]: row[tblclms[0]],
                        tblclms[1]: row[tblclms[1]],
                        tblclms[2]: row[tblclms[2]],
                        tblclms[3]: row[tblclms[3]],
                        tblclms[4]: row[tblclms[4]]
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