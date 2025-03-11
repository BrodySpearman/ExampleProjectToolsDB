from app import mysql
from flask import request, jsonify, Blueprint
from sqlalchemy import MetaData, Table, text
from app import engine
import pymysql.cursors

models_bp = Blueprint('models', __name__,
                        static_folder='static',
                        template_folder='templates')

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

# Retrieve data from the database and draw on client side.
def draw_table(tblenme):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method == 'POST':
            draw = request.form['draw']
            searchVal = request.form["search[value]"]

            print(searchVal)
            print(draw)

            # No filtering
            cursor.execute(f"SELECT * FROM {tblenme}")
            datalist = cursor.fetchall()
            record_count = cursor.rowcount

            tblclms = get_col_names(tblenme) # Collects list of column names 
            data = []

            # User input search value.
            like_string = f"\"%{searchVal}%\""

            if tblenme == 'tool':
                # Search filtered list
                if searchVal:
                    query = (f"SELECT * FROM {tblenme} WHERE "
                             f"ToolID LIKE {like_string} OR "
                             f"ToolName LIKE {like_string} OR "
                             f"Brand LIKE {like_string} OR "
                             f"Description LIKE {like_string};").replace('\n', '')
                    
                    cursor.execute(query)
                    datalist = cursor.fetchall()

                # final data formatting
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
                # Search filtered list
                if searchVal:
                    query = (f"SELECT * FROM {tblenme} WHERE "
                             f"EmployeeID LIKE {like_string} OR "
                             f"FirstName LIKE {like_string} OR "
                             f"LastName LIKE {like_string};").replace('\n', '')

                    cursor.execute(query)
                    datalist = cursor.fetchall()

                for row in datalist:
                    data.append({
                        tblclms[0]: row[tblclms[0]],
                        tblclms[1]: row[tblclms[1]],
                        tblclms[2]: row[tblclms[2]]
                    })

            if tblenme == 'checkout':
                # Search filtered list
                if searchVal:
                    query = (f"SELECT * FROM {tblenme} WHERE "
                             f"CheckoutNum LIKE {like_string} OR "
                             f"EmployeeID LIKE {like_string} OR "
                             f"ToolName LIKE {like_string};").replace('\n', '')
                    cursor.execute(query)
                    datalist = cursor.fetchall()
                    
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
                'iTotalRecords': record_count,
                'iTotalDisplayRecords': record_count,
                'aaData': data
            }
            
            print(response)
            return jsonify(response)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def strip_whitespace(data):
    for val in data.values():
        if isinstance(val, str):
            val = val.replace('/n', '').strip()
    return data

def validate_tool(data):
    special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>/?\\'
    validate_list = {
        data['data[0][ToolName]']: "ToolName",
        data['data[0][Type]']: "Type",
        data['data[0][Brand]']: "Brand", 
        data['data[0][SKU]']: "SKU",
        data['data[0][SerialNum]']: "SerialNum"
        }
    
    errors = []
    for input, field in validate_list:
        if special_chars in input:
            item_error = {
                "name": field,
                "status": "Field cannot contain special characters."
            }
            errors.append(item_error)
    
    return {errors}
    