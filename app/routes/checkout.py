from flask import Blueprint, render_template, request, jsonify
from app.models import get_col_names, engine, draw_table
import pymysql.cursors
from __init__ import mysql

checkout_table_bp = Blueprint('checkout_table', __name__, 
                                static_folder='static', 
                                template_folder='templates')

