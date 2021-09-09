from CuriousFeed import db


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
