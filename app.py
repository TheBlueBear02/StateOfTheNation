from flask import Flask, render_template, request
from datetime import datetime
import os
from pyluach import dates

app = Flask(__name__)

@app.template_global()
def static_include(filename):
    fullpath = os.path.join(app.static_folder, filename)
    with open(fullpath, 'r') as f:
        return f.read()
 

def get_date(): # return today's date
    return datetime.today().strftime('%d.%m.%Y')
def get_hebrew_date():
    today = dates.HebrewDate.today()
    return today.hebrew_date_string()

@app.route('/')
def index():
    return render_template('index.html', today_date=get_date(), hebrew_date=get_hebrew_date())

@app.route('/offices')
def offices():
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
    
    return render_template('offices.html', lables=lables, values=values)

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