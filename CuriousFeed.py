from flask import Flask

app = Flask(__name__)

@app.route("/")
def Home():
    return "<h1>Home Page</h1>"

@app.route("/video")
def Video():
    return "<h1>Todays Video</h1>"

if __name__ == '__main__':
    app.run(debug=True)