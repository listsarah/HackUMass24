from flask import Flask, request, abort
from db import get_info, set_oven_status
app = Flask(__name__)


@app.route('/')
def route():
    return "Is My House On Fire Server V 0.1"

@app.route('/upload', methods=["POST"])
def upload():
    json = request.get_json()
    code = json["code"]
    key = json["key"]
    status = json["status"] == "true"
    result = set_oven_status(code, key, status)
    if result == 200:
        return {"success": True}
    return abort(result)


@app.route('/getinfo')
def getinfo():
    code = request.args.get("code")
    return get_info(code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
