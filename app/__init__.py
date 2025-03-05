from flask import Flask
from .config import Config
from sqlalchemy import create_engine
from flaskext.mysql import MySQL

mysql = MySQL()
engine = create_engine(Config.DBURL)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['MYSQL_DATABASE_USER'] = config_class.DBUSER
    app.config['MYSQL_DATABASE_PASSWORD'] = config_class.DBPASS
    app.config['MYSQL_DATABASE_DB'] = config_class.DBNAME
    app.config['MYSQL_DATABASE_HOST'] = config_class.DBHOST
    mysql.init_app(app)

    from .routes.base import base_bp
    app.register_blueprint(base_bp)

    from .routes.tool import tool_table_bp
    app.register_blueprint(tool_table_bp)

    from .routes.checkout import checkout_table_bp
    app.register_blueprint(checkout_table_bp)

    from .routes.employee import employee_table_bp
    app.register_blueprint(employee_table_bp)
        
    if app.debug and not app.testing:
        pass

    from app import routes, models
    
    return app

