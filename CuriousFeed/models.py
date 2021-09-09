from CuriousFeed import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    link = db.Column(db.String())
    cover_image = db.Column(db.String(20), default='default.jpg')
    category = db.Column(db.String(60), nullable=False)
    approved = db.Column(db.Boolean(), default=False)
    displayed = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"Content('{self.title}', '{self.link}', '{self.cover_image}'"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
