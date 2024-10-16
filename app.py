from flask import Flask, render_template, request
from datetime import datetime
import json
from pyluach import dates
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, KnessetMembers, Tweets, Offices, Indexes, Indexes_Data  # Import the models
from routes import routes  # Import the routes Blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sn.db'

# Initialize dSb with the Flask app
db.init_app(app)
migrate = Migrate(app, db)  # This line initializes Flask-Migrate

# Register the Blueprint with the app
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
