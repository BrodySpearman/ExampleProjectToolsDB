from flask import Blueprint, render_template, request, jsonify
from ..models import get_col_names, draw_table
import pymysql.cursors
from ..__init__ import mysql

employee_table_bp = Blueprint('employee_table_bp', __name__,
                                static_folder='static',
                                template_folder='templates')

@employee_table_bp.route('/employees', methods = ['GET', 'POST'])
def employees():
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

            cmd = "INSERT INTO employee (EmployeeID, FirstName, LastName) VALUES (%s, %s, %s)"
            cursor.execute(cmd, (data['data[0][EmployeeID]'], data['data[0][FirstName]'], data['data[0][LastName]']))
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
                    cmd = "DELETE FROM employee WHERE EmployeeID = %s"
                    cursor.execute(cmd, (id))
                    conn.commit()
                response = { }
                print('Records deleted.')
                return jsonify(response)

            else:
                data = request.form.to_dict(flat=True)
                print(data)

                cmd = "DELETE FROM employee WHERE EmployeeID = %s"
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