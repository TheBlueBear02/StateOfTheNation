from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

def get_date(): # return today's date
    return datetime.today().strftime('%d.%m.%Y')

@app.route('/')
def home():
    return render_template('offices.html', today_date=get_date())

if __name__ == '__main__':
    app.run(debug=True)


 