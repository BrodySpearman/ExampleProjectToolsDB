from flask import Blueprint, render_template

base_bp = Blueprint('base', __name__,
                    static_folder='static',
                    template_folder='templates')

@base_bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('base.html')
