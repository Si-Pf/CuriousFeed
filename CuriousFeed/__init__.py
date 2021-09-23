from logging import raiseExceptions
from sqlalchemy.sql.expression import func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY']='3339113568fcc3ffbc52cbca182d8c62'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
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
        print(video.title + ' activated')
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
        print(podcast.title + ' activated')
        db.session.commit()
    else:
        print('No new Podcasts available')
    return
