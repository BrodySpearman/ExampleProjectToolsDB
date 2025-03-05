from flask import Blueprint, render_template, request, jsonify
from ..models import get_col_names, draw_table

checkout_table_bp = Blueprint('checkout_table_bp', __name__, 
                                static_folder='static', 
                                template_folder='templates')

@checkout_table_bp.route('/checkouts', methods = ['GET', 'POST'])
def checkouts():
    checkout_table_cols = get_col_names('checkout')
    return render_template('checkout_table.html', checkout_table_cols=checkout_table_cols)

@checkout_table_bp.route('/ajaxcheckouts', methods = ['GET', 'POST'])
def ajaxcheckouts():
    return draw_table('checkout')

@checkout_table_bp.route('/add_checkout', methods = ['GET', 'POST'])
def add_checkout():
    pass
