from flask import Flask, render_template, request, jsonify, send_from_directory

from threading import Thread
import os

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
                               
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)