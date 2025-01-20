from flask import Flask, render_template, request, redirect, url_for, Response, session
import json, time, os
from core import api
from datetime import datetime

app = Flask("citymonitor")
app.config['SECRET_KEY'] = 'citymonitor'
app.config['ADMIN_USERNAME'] = 'admin'
app.config['ADMIN_PASSWORD'] = 'admin'



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

with open(os.path.join('static', 'saved.json'), 'r') as f:
    saved = json.load(f)
"""    for entry in saved:
        print(entry['route'], entry['stop_id'])"""


def get_eta_countdown(stop):
    countdown = api.get_eta(stop['stop_id'], stop['route'], "countdown")
    return float('inf') if countdown == "N/A" else (0 if countdown == "Now" else int(countdown))

@app.route('/')
def home():
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    date = f"{day}/{month}"
    current_time = datetime.now()
    hours = current_time.hour % 12
    if hours == 0:
        hours = 12
    minutes = current_time.minute
    time = f"{hours}:{minutes:02}"
    sorted_saved = sorted(saved, key=get_eta_countdown)
    return render_template("index.html", saved=sorted_saved, api=api, time=time, date=date)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    date = f"{day}/{month}"
    current_time = datetime.now()
    hours = current_time.hour % 12
    if hours == 0:
        hours = 12
    minutes = current_time.minute
    time = f"{hours}:{minutes:02}"
    if 'logged_in' not in session:
        auth = request.authorization
        if not auth or auth.username != app.config['ADMIN_USERNAME'] or auth.password != app.config['ADMIN_PASSWORD']:
            return Response(
                'Could not verify your login!', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        session['logged_in'] = True
    if request.method == 'POST':
        global saved
        new_saved = []
        for i in range(len(saved)):
            route = request.form.get(f'route_{i+1}')
            stop_id = request.form.get(f'stop_id_{i+1}')
            new_saved.append({"route": route, "stop_id": stop_id})
        with open(os.path.join('static', 'saved.json'), 'w') as f:
            json.dump(new_saved, f, indent=4)
        with open(os.path.join('static', 'saved.json'), 'r') as f:
            saved = json.load(f)
        return redirect(url_for('admin'))
    return render_template("admin.html", saved=saved, date=date, time=time)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)