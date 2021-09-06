from flask import render_template, flash, redirect
from flask.helpers import url_for
from CuriousFeed import app
from CuriousFeed.models import Content
from CuriousFeed.forms import SubmitMediaForm

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


@app.route("/submit_media", methods=['GET', 'POST'])
def Submit():
    form = SubmitMediaForm()
    if form.validate_on_submit():
        flash(f'{form.title.data} successfully submitted!', 'success')
        return redirect(url_for('Home'))
    return render_template('submit_media.html', title='Submit your media', form = form)

