from flask import Flask, render_template, request
from .. import botDB

app = Flask(__name__, static_folder='static', template_folder="templates")
code = ""


@app.route('/', methods=['POST'])
def getData():
    value: str = request.form.get("username")
    global code
    print(code, value)
    if value:
        print(botDB.checkIfAlreadyInserted(value))
    return "Your username has been saved"


# def sendData(value):
#     requests.post(link,
#                   data={value},
#                   )
@app.route('/', methods=['GET'])
def index():
    global code
    value = request.args.get('code')
    code = value
    print(code)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=False)
