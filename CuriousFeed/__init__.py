from logging import raiseExceptions
from sqlalchemy.sql.expression import func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY']='3339113568fcc3ffbc52cbca182d8c62'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_final.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'Login'

from CuriousFeed import routes

from CuriousFeed import db
from CuriousFeed.models import Content
from sqlalchemy.sql.expression import func

@app.cli.command()
def scheduled():
    """Run scheduled jobs"""
    print('Updating daily content:')
    
    #Randomly select new video
    video = Content.query.filter(Content.category == "Video", Content.displayed == False, Content.approved == True).order_by(func.random()).first()
    if video:
        video_old = Content.query.filter(Content.active == True, Content.category == "Video").first()
        if video_old:
            video_old.active = False
        video.displayed = True
        video.active = True
        print('video ' + video.title + ' activated')
        db.session.commit()
    else:
        print('No new Videos available')

    #Randomly select new podcast
    podcast = Content.query.filter(Content.category == "Podcast", Content.displayed == False, Content.approved == True).order_by(func.random()).first()
    if podcast:
        podcast_old = Content.query.filter(Content.active == True, Content.category == "Podcast").first()
        if podcast_old:
            podcast_old.active = False        
        podcast.displayed = True
        podcast.active = True
        print('podcast ' +podcast.title + ' activated')
        db.session.commit()
    else:
        print('No new Podcasts available')

    #Randomly select new book
    book = Content.query.filter(Content.category == "Book", Content.displayed == False, Content.approved == True).order_by(func.random()).first()
    if book:
        book_old = Content.query.filter(Content.active == True, Content.category == "Book").first()
        if book_old:
            book_old.active = False        
        book.displayed = True
        book.active = True
        print('book ' +book.title + ' activated')
        db.session.commit()
    else:
        print('No new books available')

    return
