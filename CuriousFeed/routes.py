from flask import render_template, flash, redirect, request
from flask.helpers import url_for
from urllib.parse import urlparse, parse_qs
from CuriousFeed import app, db, bcrypt, mail
from CuriousFeed.models import Content, User, Feedback
from CuriousFeed.forms import SubmitMediaForm, LoginForm, FeedbackForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from isbnlib import canonical, to_isbn10, meta
from datetime import datetime
import os
import re

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

def get_isbn_10(isbn):
    if len(canonical(isbn)) == 13:
        return to_isbn10(isbn)
    else: 
        return isbn




@app.route("/")
def Home():
#    return render_template('home.html')
    return render_template('home_count.html')    

@app.route("/video")
def Video():
    video = Content.query.filter(Content.category == "Video", Content.active == True).first()
    video.link = "http://www.youtube.com/embed/"+get_video_id(video.link)+"?modestbranding=1"
    return render_template('video.html', video = video)

@app.route("/book")
def Book():
    book = Content.query.filter(Content.category == "Book", Content.active == True).first()
    isbn = get_isbn_10(book.link)
    book.link = "https://lesen.amazon.de/kp/card?asin="+ isbn +"&preview=inline&linkCode=kpe&hideBuy=true&hideShare=true"
    data = meta(isbn)
    data['Author'] = data['Authors'][0]
    return render_template('book.html', book = book, isbn = isbn, data = data)


@app.route("/podcast")
def Podcast():
    podcast = Content.query.filter(Content.category == "Podcast", Content.active == True).first()
    podcast.link = "https://open.spotify.com/embed-podcast/episode/"+get_podcast_id(podcast.link)
    return render_template('podcast.html', podcast = podcast)


@app.route("/submit_media", methods=['GET', 'POST'])
def Submit():
    form = SubmitMediaForm()
    # Extract Youtube ID from URL



    if form.validate_on_submit():
        #if form.category.data =="Video":
        reason = re.sub(r'http\S+', '*Link removed for security reasons*', form.reason.data)

        content = Content(reason = reason, category = form.category.data, link = form.link.data, recommended_by_age = form.age.data, recommended_by_name = form.name.data, title = form.keywords.data)

  #      elif form.category.data =="Podcast":
   #         content = Content(reason = form.reason.data, category = form.category.data, link = form.link.data)
            
    #    else:
     #       content = Content(reason = form.reason.data, category = form.category.data, link = form.link.data)
            
        db.session.add(content)
        db.session.commit()
        flash(f'{form.link.data} successfully submitted for review!', 'success')
        return redirect(url_for('Home'))
    return render_template('submit_media.html', title='Submit your media', form = form)

@app.route("/admin-portal")
@login_required
def Admin():
    return render_template('admin.html', content = Content.query.all())




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


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def Edit(id):
    qry = db.session.query(Content).filter(
                Content.content_id==id)
    item = qry.first()
    if item.approved == False:
        item.approved = True
    
    else:
        item.approved = False

    db.session.commit()
    
    return redirect(url_for('Admin'))

@app.route("/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def Delete(id):
    db.session.query(Content).filter(
                Content.content_id==id).delete()

    db.session.commit()
    
    return redirect(url_for('Admin'))


@app.route("/logout")
def Logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/impressum")
def Impressum():
    return render_template("impressum.html")

@app.route("/feedback", methods=['GET', 'POST'])
def Feedback_form():
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback(feedback = form.feedback.data, sent_on = datetime.now())
        msg = Message('New feedback was submitted to CuriousFeed', sender = "bot@curiousfeed.de", recipients=[os.environ.get('FEEDBACK_TO')])
        msg.body = "New feedback: "+ form.feedback.data
        mail.send(msg)
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback succesfully submitted', 'success')
        return redirect(url_for('Home'))
    
    return render_template('feedback.html', title='Feedback', form=form)


