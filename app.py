from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import routes  # Import the routes Blueprint
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'sn.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

# Initialize dSb with the Flask app
db.init_app(app)

migrate = Migrate(app, db)  # This line initializes Flask-Migrate

# Register the Blueprint with the app
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
