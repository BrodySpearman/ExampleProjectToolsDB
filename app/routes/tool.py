from flask import Blueprint, render_template, request, jsonify
from ..models import get_col_names, draw_table, strip_whitespace, validate_tool
import pymysql.cursors
from app import mysql

tool_table_bp = Blueprint('tool_table_bp', __name__, 
                            static_folder='static', 
                            template_folder='templates')

@tool_table_bp.route('/tools', methods=('GET', 'POST'))
def tools():
    tool_table_cols = get_col_names('tool')
    return render_template('tool_table.html', tool_table_cols=tool_table_cols)

@tool_table_bp.route('/ajaxtools', methods = ['GET', 'POST'])
def ajaxtools():
    return draw_table('tool')

@tool_table_bp.route('/create_tool', methods = ['GET', 'POST'])
def create_new_tool():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method == 'POST':
            raw_data = request.form.to_dict(flat=True)
            # Client form example (ImmutableMultiDict):
            # ([('data[0][ToolID]', 'value'), ('data[0][Type]', 'value'), ('data[0][ToolName]', 'value'), 
            # ('data[0][Brand]', 'value'), ('data[0][SKU]', 'value'), ('data[0][SerialNum]', 'value'), 
            # ('data[0][Description]', 'value'), ('action', 'create')]
            
            # Validating client data
            data = strip_whitespace(raw_data)
            validation = validate_tool(data)

            print(data)
            cmd = "INSERT INTO tool (ToolID, Type, ToolName, Brand, SKU, SerialNum, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(cmd, (data['data[0][ToolID]'], data['data[0][Type]'], data['data[0][ToolName]'],
                                 data['data[0][Brand]'], data['data[0][SKU]'], data['data[0][SerialNum]'],
                                 data['data[0][Description]']))
            conn.commit()

            response_data = {
                'ToolID': data['data[0][ToolID]'],
                'Type': data['data[0][Type]'],
                'ToolName': data['data[0][ToolName]'],
                'Brand': data['data[0][Brand]'],
                'SKU': data['data[0][SKU]'],
                'SerialNum': data['data[0][SerialNum]'],
                'Description': data['data[0][Description]']
            }

            response = {
                'data': response_data
            }

            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@tool_table_bp.route('/delete_tool/<_id_>', methods = ['DELETE'])
def delete_tool(_id_):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method == 'DELETE':

            if "," in _id_: # If multiple ids are passed.
                id_list = [int(x) for x in _id_.split(",")]
                data = request.form.to_dict(flat=True)
                print(id_list)

                for id in id_list:
                    cmd = "DELETE FROM tool WHERE ToolID = %s"
                    cursor.execute(cmd, (id))
                    conn.commit()
                response = { }
                print('Records deleted.')
                return jsonify(response)

            else:
                data = request.form.to_dict(flat=True)
                print(data)

                cmd = "DELETE FROM tool WHERE ToolID = %s"
                cursor.execute(cmd, (_id_))
                conn.commit()

                response = { }
                print('Record deleted.')
                return jsonify(response)
    
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()