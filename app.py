from flask import Flask, render_template, request
from datetime import datetime
import json
from pyluach import dates
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sn.db'

# Configuration for the PostgreSQL database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:2311@localhost/State of the Nation'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database connection
db = SQLAlchemy(app)

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

class Offices(db.Model):
    id = db.Column(db.Integer, nullable=False,primary_key=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.String)
    minister_id = db.Column(db.Integer, nullable=False)
    deputy_minister_id = db.Column(db.Integer)

def get_date(): # return today's date
    return datetime.today().strftime('%d.%m.%Y')
def get_hebrew_date(): # return hebrew date
    today = dates.HebrewDate.today()
    return today.hebrew_date_string()

@app.route('/add_data', methods=['POST'])
def add_km():
    # Read the JSON data
    with open(r'E:\Development Projects\SN\DB\KnessetMembers.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate through each entry in the JSON and add it to the database
    for entry in data['Members']:
        new_message = KnessetMembers(
            km_id=entry['Id'],
            party=entry['party'],
            is_coalition=entry['is_coalition'],
            image=entry['image'],
            additional_role=entry['additional_role'],
            name=entry['name']
        )
        db.session.add(new_message)
    
    # Commit the changes to the database
    db.session.commit()
    return 'Data added successfully'
@app.route('/add_data', methods=['POST'])
def add_tweet():
    # Read the JSON data
    with open(r"E:\Development Projects\SN\DB\Tweets.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate through each entry in the JSON and add it to the database
    for entry in data:
        new_message = Tweets(
            id=entry['Id'],
            km_id=entry['UserId'],
            text=entry['Text'],
            date=entry['Date'],
            time=entry['Time'],
            topic=entry['Topic']
        )
        db.session.add(new_message)
    
    # Commit the changes to the database
    db.session.commit()
    return 'Data added successfully'

@app.route('/')
def index():
    # Query the database for all users
    all_tweets = db.session.query(Tweets).all()
    all_kms = db.session.query(KnessetMembers).all()
    
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
            'image': image,
            'additional_role': additional_role
        }
        tweets.append(tweet_data)

    return render_template('index.html', today_date=get_date(), hebrew_date=get_hebrew_date(), tweets=reversed(tweets))

@app.route('/offices')
def offices():
    all_offices = db.session.query(Offices).all()
    all_kms = db.session.query(KnessetMembers).all()

    offices_list = []
    name=""
    party=""
    image=""
    additional_role=""
    number_of_offices = 4
    i=0

    for office in all_offices:
        if i == 4:
            break
        for member in all_kms:
            if member.km_id == office.minister_id:
                name = member.name
                party = member.party
                image = member.image
                additional_role = member.additional_role
                break
        office_data = {
            'name':office.name,
            'info': office.info,
            'minister_name': name,
            'minister_image': image,  
            'minister_party': party,
            'minister_role': additional_role,
        }
        offices_list.append(office_data)
        i += 1

    data = [
        ("ינואר 2020", 1597),
        ("פברואר 2020", 1457),
        ("מרץ 2020", 1997),
        ("אפריל 2020", 879),
        ("מאי 2020", 784),
        ("יוני 2020", 456),
        ("יולי 2020", 1100),
        ("2020 אוגוסט", 1235),
        ("ספטמבר 2020", 1476),
        ("אוקטובר 2020", 1597),
        ("נובמבר 2020", 1457),
        ("דצמבר 2020", 1997),
        ("ינואר 2021", 879),
        ("פברואר 2021", 784),
        ("מרץ 2021", 456),
        ("אפריל 2021", 1100),
        ("מאי 2021", 1235),
        ("יוני 2021", 1476),
    ]
    lables = []
    values = []
    for row in data:
        lables.append(row[0])
        values.append(row[1])
    
    return render_template('offices.html', lables=lables, values=values, offices=offices_list)

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
    lables = []
    values = []
    for row in data:
        lables.append(row[0])
        values.append(row[1])

    return render_template('economy.html', lables=lables, values=values)

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
