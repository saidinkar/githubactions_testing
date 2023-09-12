'''This is a module-level docstring that describes the purpose of the app.py module.'''


from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello Arch world!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
