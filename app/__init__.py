from flask import Flask
from ..config import Config
from .routes import base as main_blueprint, tool as tool_table_bp, checkout as checkout_table_bp, employee as employee_table_bp
from .models import init_db
from flaskext.mysql import MySQL

mysql = MySQL()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['MYSQL_DATABASE_USER'] = Config.dbuser
    app.config['MYSQL_DATABASE_PASSWORD'] = Config.dbpass
    app.config['MYSQL_DATABASE_DB'] = Config.dbname
    app.config['MYSQL_DATABASE_HOST'] = Config.dbhost
    init_db(app=app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(tool_table_bp)
    app.register_blueprint(checkout_table_bp)
    app.register_blueprint(employee_table_bp)
    

    if app.debug and not app.testing:
        pass
    
    return app

from app import routes, models
