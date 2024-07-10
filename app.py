from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def get_date(): # return today's date
    return datetime.today().strftime('%d.%m.%Y')

@app.route('/')
def index():
    return render_template('index.html', today_date=get_date())

@app.route('/offices')
def offices():
    return render_template('offices.html', today_date=get_date())

@app.route('/demography')
def demography():
    return render_template('demography.html', today_date=get_date())

if __name__ == '__main__':
    app.run(debug=True)