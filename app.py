from configparser import ConfigParser
from flask import Flask, render_template, request, redirect, Response
from url import initialize_database, get_url, get_url_id, short_url

app = Flask(__name__)
config = ConfigParser()
config.read('config.ini')


@app.route('/', methods=["GET"])
def home():
    id = request.args.get("id")
    if id:
        if id.isdigit():
            url = get_url(int(id))
        if url:
            return redirect(url)

    # If the id and url parameters doesn't exist, return the home page
        return Response('<h1>Invalid Url</h1>', status=404)

    url = request.args.get("url")
    if url:
        shorten_url = short_url(url.strip())

        return render_template('index.html', url=shorten_url)

    return render_template('index.html')


if __name__ == "__main__":
    DEBUG = config["APP"]["DEBUG"]
    HOST = config["DATABASE"]["HOST"]
    PORT = config["DATABASE"]["PORT"]
    app.run(debug=DEBUG, host=HOST, port=PORT)
