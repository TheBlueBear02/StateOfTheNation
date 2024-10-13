from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class KnessetMembers(db.Model):
    km_id = db.Column(db.Integer, nullable=False,primary_key=True)
    party = db.Column(db.String, nullable=False)
    is_coalition = db.Column(db.Boolean, nullable=False) 
    image = db.Column(db.String)
    additional_role = db.Column(db.String, nullable=False) 
    name = db.Column(db.String(80), unique=False, nullable=False)

class Tweets(db.Model):
    id = db.Column(db.Integer, nullable=False,primary_key=True)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False,)
    time = db.Column(db.String, nullable=False,)
    topic = db.Column(db.String, nullable=False,)
    km_id = db.Column(db.Integer, nullable=False,)
    image = db.Column(db.String)

class Offices(db.Model):
    id = db.Column(db.Integer, nullable=False,primary_key=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.String)
    minister_id = db.Column(db.Integer, nullable=False)
    deputy_minister_id = db.Column(db.Integer)

class Indexes(db.Model):
    id = db.Column(db.Integer, nullable=False,primary_key=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.String)
    office_id = db.Column(db.Integer, nullable=False)
    is_kpi = db.Column(db.Boolean, nullable=False)
    icon = db.Column(db.String)
    alert = db.Column(db.Boolean)
    chart_type = db.Column(db.String)

class Indexes_Data(db.Model):
    id = db.Column(db.Integer, nullable=False,primary_key=True)
    index_id = db.Column(db.String, nullable=False)
    label = db.Column(db.String)
    value = db.Column(db.Integer, nullable=False)

