from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api", methods=["POST"])
def getData():
    data = request.json
    print(data)
    return "", 200


app.route("/get_my_ip", methods=["GET"])


def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9002, debug=False)
