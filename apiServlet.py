from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    print("GET")
    return jsonify({'message': 'Hello, World!'})


@app.route('/', methods=['POST'])
def getData():
    # type = request.args.get('data')
    value = request.view_args
    print(value)


if __name__ == "__main__":
    app.run(debug=True)
