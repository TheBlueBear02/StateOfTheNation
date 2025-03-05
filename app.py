import os
from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import index_bp, offices_bp, demography_bp, economy_bp, parliament_bp, info_bp

# Create the app factory
def create_app(config_class=None):
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(offices_bp)
    app.register_blueprint(demography_bp)
    app.register_blueprint(economy_bp)
    app.register_blueprint(parliament_bp)
    app.register_blueprint(info_bp)

    app.secret_key = "pass"  # Change this to a strong, unique key

    # Set default configuration or override it with a provided config class
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'sn.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications
    
    if config_class:
        app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db, compare_type=True)

    
    return app
