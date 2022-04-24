from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
app.config["EXPLAIN_TEMPLATE_LOADING"] = True

@app.route('/', methods=['POST'])
def getData():
    # type = request.args.get('data')
    value = request.view_args
    print(value)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
