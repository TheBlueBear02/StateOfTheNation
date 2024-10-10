from collections import namedtuple
from flask import Flask, render_template, request
from datetime import datetime
import json
from pyluach import dates
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sn.db'

# Configuration for the PostgreSQL database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:2311@localhost/State of the Nation'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def get_date(): # return today's date
    return datetime.today().strftime('%d.%m.%Y')
def get_hebrew_date(): # return hebrew date
    today = dates.HebrewDate.today()
    return today.hebrew_date_string()

# Initialize the database connection
db = SQLAlchemy(app)

migrate = Migrate(app, db)  # This line initializes Flask-Migrate

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
    date = db.Column(db.String)
    value = db.Column(db.Integer, nullable=False)



@app.route('/')
def index():
    # Query the database for all tweets and kms
    all_tweets = db.session.query(Tweets).all()
    all_kms = db.session.query(KnessetMembers).all()
    
    # create list of dicts that contains the feed's tweets
    name = ""
    party = ""
    is_coalition = False
    image = ""
    additional_role = ""
    tweets = []
    for tweet in all_tweets:
        for member in all_kms:
            if member.km_id == tweet.km_id:
                name = member.name
                party = member.party
                is_coalition = member.is_coalition
                image = member.image
                additional_role = member.additional_role
                break
        tweet_data = {
            'id':tweet.id,
            'text': tweet.text,
            'date': tweet.date,
            'time': tweet.time,
            'topic': tweet.topic,  
            'name': name,
            'party': party,
            'is_coalition': is_coalition,
            'minister_image': image,
            'additional_role': additional_role,
            'image': tweet.image
        }
        tweets.append(tweet_data)
    return render_template('index.html', today_date=get_date(), hebrew_date=get_hebrew_date(), tweets=reversed(tweets))

Cell = namedtuple("cell", ["css_class", "size", "is_placeholder", "alert", "name"])

@app.route('/offices')
def offices():
    all_offices = db.session.query(Offices).all()
    all_kms = db.session.query(KnessetMembers).all()
    # save the first 4 offices from the database and their ministers data in a list
    offices_list = []
    number_of_offices = 4
    i=0

    cells = [[Cell("kpi_bubble", 3.5, False, False, 'name'), Cell("kpi_bubble", 4.5, False,False, 'name')]]

    for office in all_offices:
        if i == number_of_offices:
            break
        minister = db.session.query(KnessetMembers).filter_by(km_id=office.minister_id).first()
            
        office_data = {
            'name':office.name,
            'info': office.info,
            'minister_name': minister.name,
            'minister_image': minister.image,  
            'minister_party': minister.party,
            'minister_role': minister.additional_role,
        }
        offices_list.append(office_data)
        i += 1

    first_office_indexes = db.session.query(Indexes).filter_by(office_id='3').order_by(Indexes.is_kpi.desc()).all()
    second_office_indexes = db.session.query(Indexes).filter_by(office_id='2').all()
    third_office_indexes = db.session.query(Indexes).filter_by(office_id='3').all()
    forth_office_indexes = db.session.query(Indexes).filter_by(office_id='4').all()

    first_office_indexes_info = []
    for index in first_office_indexes:
        index_data = db.session.query(Indexes_Data).filter_by(index_id=index.id).all()
        
        lables = []
        values = []
        for row in index_data:
            lables.append(row.date)
            values.append(row.value)
        
        index_info = {
            'name':index.name,
            'info':index.info,
            'icon':index.icon,
            'is_kpi':index.is_kpi,
            'alert':index.alert,
            'chart_type':index.chart_type,
            'lables': lables,
            'values': values
        }
        first_office_indexes_info.append(index_info)
    return render_template('offices.html', values=values,lables=lables,offices=offices_list, first_office_indexes=first_office_indexes_info, cells=cells)

@app.route('/demography')
def demography():
    data = [
        ("1948", 100000),
        ("1950", 300000),
        ("1954", 500000),
        ("1960", 800000),
        ("1966", 1000000),
        ("1970", 1500000),
        ("1976", 2000000),
        ("1982", 2500000),
        ("1988", 3200000),
        ("1994", 4000000),
        ("2000", 4800000),
        ("2006", 5700000),
        ("2012", 6700000),
        ("2018", 8000000),
        ("2023", 8600000),
        ("2024", 9900000),
    ]
    lables = []
    values = []
    for row in data:
        lables.append(row[0])
        values.append(row[1])
    
    return render_template('demography.html', lables=lables, values=values)


@app.route('/economy')
def economy():
    data = [
        ("מע'מ",98.8),
        ("מס הכנסה  על יחידים",92.6),
        ("ביטוח לאומי",70.8),
        ("מס חברות",38.8),
        ("רשויות מקומיות",35.2),
        ("דלקים",17.2),
        ("מע'מ על שכר",15.7),
        ("מיסי נדלן",11.4),
        ("כלי רכב",9.7),
        ("אחר",26.4),
    ]
    # Main Graph data
    main_labels = []
    main_values = []
    temp_values = []
    
    debt_per_year = db.session.query(Indexes_Data).filter_by(index_id=5).all()
    income_per_year = db.session.query(Indexes_Data).filter_by(index_id=6).all()
    expenses_per_year = db.session.query(Indexes_Data).filter_by(index_id=7).all()
    interest_per_year = db.session.query(Indexes_Data).filter_by(index_id=8).all()
    gdp_per_year = db.session.query(Indexes_Data).filter_by(index_id=9).all()

    indexes = []
    indexes.append(debt_per_year)
    indexes.append(income_per_year)
    indexes.append(expenses_per_year)
    indexes.append(interest_per_year)
    indexes.append(gdp_per_year)


    for row in income_per_year:
        main_labels.append(row.date)

    for index in indexes:
        for row in index:
            temp_values.append(row.value)
        main_values.append(temp_values)
        temp_values = []

    lables = []
    values = []
    for row in data:
        lables.append(row[0])
        values.append(row[1])

    return render_template('economy.html', main_lables=main_labels, main_values=main_values)

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
