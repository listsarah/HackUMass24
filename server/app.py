from flask import Flask, request, abort
from db import get_info, set_oven_status
from model import is_on
app = Flask(__name__)


@app.route('/')
def route():
    return "Is My House On Fire Server V 0.1"

@app.route('/upload', methods=["POST"])
def upload():
    json = request.get_json()
    code = json["code"]
    key = json["key"]
    if len(request.files) == 0:
        return abort(400)

    file = next(iter(request.files.values()))

    if file.filename == '':
        return abort(400)

    if not file:
        return abort(400)

    status = is_on(file)
    result = set_oven_status(code, key, status)
    if result == 200:
        return {"success": True}
    return abort(result)


@app.route('/getinfo')
def getinfo():
    code = request.get_json()["code"]
    return get_info(code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
