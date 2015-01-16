import datetime

from flask import Flask


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World! The server time is %s" % datetime.datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    app.run()
