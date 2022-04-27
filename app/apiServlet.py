from flask import Flask, request, render_template
import requests
# link = os.environ['home_link']

app = Flask(__name__)
app.config["EXPLAIN_TEMPLATE_LOADING"] = True

@app.route('/', methods=["GET"])
def getData():
    # type = request.args.get('data')
    value = request.args.get('code')
    # sendData(value)
    return "a"
# def sendData(value):
#     requests.post(link,
#                   data={value},
#                   )
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
