from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    link = db.Column(db.String())
    cover_image = db.Column(db.String(20), default='default.jpg')
    category = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Content('{self.title}', '{self.link}', '{self.cover_image}'"

@app.route("/")
def Home():
    return "<h1>Home Page</h1>"

@app.route("/video")
def Video():
    return "<h1>Todays Video</h1>"

if __name__ == '__main__':
    app.run(debug=True)