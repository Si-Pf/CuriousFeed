from flask import render_template, flash, redirect, request
from flask.helpers import url_for
from urllib.parse import urlparse, parse_qs
from CuriousFeed import app, db, bcrypt
from CuriousFeed.models import Content, User
from CuriousFeed.forms import SubmitMediaForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

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
    return render_template('podcast.html', podcast = Content.query.filter(Content.category == "Podcast").first())


@app.route("/submit_media", methods=['GET', 'POST'])
def Submit():
    form = SubmitMediaForm()
    # Extract Youtube ID from URL
    def get_video_id(video):
        u_pars = urlparse(video)
        quer_v = parse_qs(u_pars.query).get('v')
        if quer_v:
            return quer_v[0]
        pth = u_pars.path.split('/')
        if pth:
            return pth[-1]

    def get_podcast_id(podcast):
        id = podcast.rpartition('/')[-1]
        return id


    if form.validate_on_submit():
        if form.category.data =="Video":
            content = Content(title = form.title.data, category = form.category.data, link = "http://www.youtube.com/embed/"+get_video_id(form.link.data)+"?modestbranding=1")

        elif form.category.data =="Podcast":
            content = Content(title = form.title.data, category = form.category.data, link = "https://open.spotify.com/embed-podcast/episode/"+get_podcast_id(form.link.data))
            
        else:
            content = Content(title = form.title.data, category = form.category.data, link = form.link.data)
            
        db.session.add(content)
        db.session.commit()
        flash(f'{form.title.data} successfully submitted for review!', 'success')
        return redirect(url_for('Home'))
    return render_template('submit_media.html', title='Submit your media', form = form)

@app.route("/admin-portal")
@login_required
def Admin():
    return render_template('admin.html')




@app.route("/login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def Logout():
    logout_user()
    return redirect(url_for('home'))