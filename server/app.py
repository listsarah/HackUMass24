from flask import Flask, request, abort
from db import get_info, set_oven_status
from model import is_on
app = Flask(__name__)


@app.route('/')
def route():
    return "Is My House On Fire Server V 0.1"

@app.route('/upload', methods=["POST"])
def upload():
    code = request.form.get("code")
    key = request.form.get("key")
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

    get_info()


if __name__ == '__main__':
    app.run()
