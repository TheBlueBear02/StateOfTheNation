from flask import Flask, render_template, request
from datetime import datetime
import os


app = Flask(__name__)

@app.template_global()
def static_include(filename):
    fullpath = os.path.join(app.static_folder, filename)
    with open(fullpath, 'r') as f:
        return f.read()
 

def get_date(): # return today's date
    return datetime.today().strftime('%d.%m.%Y')

@app.route('/')
def index():
    return render_template('index.html', today_date=get_date())

@app.route('/offices')
def offices():
    data = [
        ("01-01-2020", 1597),
        ("02-01-2020", 1457),
        ("03-01-2020", 1997),
        ("04-01-2020", 879),
        ("05-01-2020", 784),
        ("06-01-2020", 456),
        ("07-01-2020", 1100),
        ("08-01-2020", 1235),
        ("09-01-2020", 1476),
        ("10-01-2020", 1597),
        ("11-01-2020", 1457),
        ("12-01-2020", 1997),
        ("13-01-2020", 879),
        ("14-01-2020", 784),
        ("15-01-2020", 456),
        ("16-01-2020", 1100),
        ("17-01-2020", 1235),
        ("18-01-2020", 1476),
    ]
    lables = []
    values = []
    for row in data:
        lables.append(row[0])
        values.append(row[1])
    
    return render_template('offices.html', lables=lables, values=values)

@app.route('/demography')
def demography():
    return render_template('demography.html')

if __name__ == '__main__':
    app.run(debug=True)