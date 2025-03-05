from flask import Blueprint, render_template, request, jsonify
from app.models import get_col_names, engine, draw_table
import pymysql.cursors
from __init__ import mysql

tool_table_bp = Blueprint('tool_table', __name__, 
                            static_folder='static', 
                            template_folder='templates')

@tool_table_bp.route('/tools', methods=('GET', 'POST'))
def tools():
    tool_table_cols = get_col_names(engine, 'tool')
    return render_template('tool_table.html', tool_table_cols=tool_table_cols)

@tool_table_bp.route('/ajaxtools', methods = ['GET', 'POST'])
def ajaxtools():
    return draw_table('tool')

@tool_table_bp.route('/create_tool', methods = ['GET', 'POST'])
def create_new_tool():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            # Client form example (ImmutableMultiDict):
            # ([('data[0][Type]', 'value'), ('data[0][ToolName]', 'value'), ('data[0][Brand]', 'value'), ('data[0][SKU]', 'value'), ('data[0][SerialNum]', 'value'), ('data[0][Description]', 'value'), ('action', 'create')])
            data = request.form.to_dict(flat=True)
            print(data)

            cursor.execute(f"""INSERT INTO tool (ToolID, Type, ToolName, Brand, SKU, SerialNum, Description) 
                            VALUES 
                            ({str(data['data[0][ToolID]'])},
                            '{str(data['data[0][Type]'])}',
                            '{str(data['data[0][ToolName]'])}',
                            '{str(data['data[0][Brand]'])}',
                            '{str(data['data[0][SKU]'])}',
                            '{str(data['data[0][SerialNum]'])}',
                            '{str(data['data[0][Description]'])}')""")
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

@tool_table_bp.route('/delete_tool/<_id_>', methods = ['DELETE'])
def delete_tool(_id_):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'DELETE':

            if "," in _id_: # If multiple ids are passed.
                id_list = [int(x) for x in _id_.split(",")]
                data = request.form.to_dict(flat=True)
                print(id_list)

                for id in id_list:
                    cursor.execute(f"DELETE FROM tool WHERE ToolID = {id}")
                    conn.commit()
                response = { }
                print('Records deleted.')
                return jsonify(response)

            else:
                data = request.form.to_dict(flat=True)
                print(data)

                cursor.execute(f"DELETE FROM tool WHERE ToolID = {int(_id_)}")
                conn.commit()

                response = { }
                print('Record deleted.')
                return jsonify(response)
    
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()