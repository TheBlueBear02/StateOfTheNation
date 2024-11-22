import os
from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import routes  # Import the routes Blueprint

# Create the app factory
def create_app(config_class=None):
    app = Flask(__name__)
    
    # Set default configuration or override it with a provided config class
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'sn.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications
    
    if config_class:
        app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # Register Blueprints
    app.register_blueprint(routes)
    
    return app
