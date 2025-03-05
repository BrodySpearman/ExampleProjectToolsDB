from flask import Blueprint, render_template, request, jsonify
from app.models import get_col_names, engine, draw_table
import pymysql.cursors
from __init__ import mysql

employee_table_bp = Blueprint('employee_table', __name__,
                                static_folder='static',
                                template_folder='templates')

@employee_table_bp.route('/employees', methods = ['GET', 'POST'])
def employee_table_show():
    employee_table_cols = get_col_names('employee')
    return render_template('employee_table.html', employee_table_cols=employee_table_cols)

@employee_table_bp.route('/ajaxemployees', methods = ['GET', 'POST'])
def ajaxemployees():
    return draw_table('employee')

@employee_table_bp.route('/create_employee', methods = ['GET', 'POST'])
def create_new_employee():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            print(request.form)
            data = request.form.to_dict(flat=True)

            cursor.execute(f"""INSERT INTO employee (EmployeeID, FirstName, LastName) 
                            VALUES 
                            ({str(data['data[0][EmployeeID]'])},
                            '{str(data['data[0][FirstName]'])}',
                            '{str(data['data[0][LastName]'])}')""")
            conn.commit()
            
            new_data = {
                'EmployeeID': data['data[0][EmployeeID]'],
                'FirstName': data['data[0][FirstName]'],
                'LastName': data['data[0][LastName]']
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

@employee_table_bp.route('/delete_employee/<_id_>', methods = ['DELETE'])
def delete_employee(_id_):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'DELETE':

            if "," in _id_: # If multiple ids are passed.
                id_list = [int(x) for x in _id_.split(",")]
                data = request.form.to_dict(flat=True)
                print(id_list)

                for id in id_list:
                    cursor.execute(f"DELETE FROM employee WHERE EmployeeID = {id}")
                    conn.commit()
                response = { }
                print('Records deleted.')
                return jsonify(response)

            else:
                data = request.form.to_dict(flat=True)
                print(data)

                cursor.execute(f"DELETE FROM employee WHERE EmployeeID = {int(_id_)}")
                conn.commit()

                response = { }
                print('Record deleted.')
                return jsonify(response)
    
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()