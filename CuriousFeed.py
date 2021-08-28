
from flask import Flask, render_template
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
    return render_template('home.html')

@app.route("/video")
def Video():
    return render_template('video.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)