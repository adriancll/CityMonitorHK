from flask import Flask, render_template, request, redirect, url_for
import requests, json, time, os
from core import api

app = Flask("citymonitor")
app.config['SECRET_KEY'] = 'citymonitor'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/admin')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)