from configparser import ConfigParser
from flask import Flask, render_template

app = Flask(__name__)
config = ConfigParser()
config.read('config.ini')


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    DEBUG = config["APP"]["DEBUG"]
    HOST = config["DATABASE"]["HOST"]
    PORT = config["DATABASE"]["PORT"]
    app.run(debug=DEBUG, host=HOST, port=PORT)
