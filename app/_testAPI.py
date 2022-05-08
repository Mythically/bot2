from flask import Flask, render_template, request
from getCurrentPublicUrlNgrok import getUrl
import os
import sys
import inspect
import requests

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import botDB

url = getUrl()

app = Flask(__name__, static_folder='static', template_folder="templates")
code = ""
link = "https://accounts.spotify.com/authorize"


# finish this
@app.route('/', methods=['POST'])
def getData():
    value: str = request.form.get("username")
    global code
    print(code, value)
    if value is not None:
        if not botDB.checkIfAlreadyInserted(value):
            data = requestAuthorization()
            access_token = data['access_token']
            refresh_token = data['refresh_token']
        else:
            return "This username is already in the database, please check your submission"
    return "Your username has been saved"


def requestAuthorization():
    response = requests.get(link,
                            data={'client_id': os.environ['90082084b6b6423f8f08dd85e74f42b4'],
                                  'response_type': 'code',
                                  'redirect_uri': 'https://mythicalapi.pythonanywhere.com',
                                  'scope': 'user-read-currently-playing'},
                            ).json()
    data = [response['access_token'], response['refresh_token']]


@app.route('/', methods=['GET'])
def index():
    global code
    value = request.args.get('code')
    code = value
    print(code)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host=f"{url}]", port=80, debug=False)
