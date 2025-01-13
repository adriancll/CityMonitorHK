from flask import Flask, render_template
import json, time, os
from core import api
from datetime import datetime

app = Flask("citymonitor")
app.config['SECRET_KEY'] = 'citymonitor'

def time():
    current_time = datetime.now()
    hours = current_time.hour % 12
    if hours == 0:
        hours = 12
    minutes = current_time.minute
    return f"{hours}:{minutes:02}"

def date():
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    return f"{day}/{month}"

date = date()
time = time()
        
with open(os.path.join('static', 'saved.json'), 'r') as f:
    saved = json.load(f)
"""    for entry in saved:
        print(entry['route'], entry['stop_id'])"""


@app.route('/')
def home():
    return render_template("index.html",saved=saved, api=api, time=time, date=date)

@app.route('/admin')
def admin():
    return api.get_eta("002972", "8X", "time")


if __name__ == '__main__':
    app.run(debug=True, port=5000)