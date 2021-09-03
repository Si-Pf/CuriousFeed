from flask import render_template
from CuriousFeed import app
from CuriousFeed.models import Content

@app.route("/")
def Home():
    return render_template('home.html')

@app.route("/video")
def Video():
    return render_template('video.html', video = Content.query.filter(Content.category == "Video").first())

@app.route("/book")
def Book():
    return render_template('book.html')


@app.route("/podcast")
def Podcast():
    return render_template('podcast.html')


@app.route("/submit_media")
def Submit():
    return render_template('submit_media.html')