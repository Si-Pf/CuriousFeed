from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, ValidationError, URL, Optional
from CuriousFeed.models import Content
from isbnlib import notisbn
import re
import requests



class SubmitMediaForm(FlaskForm):
    reason = TextAreaField('Why do you recommend this? Give a few short sentences why this is worth watching/listening/reading', 
                        validators= [DataRequired(), Length(min=10, max=400)])

    category = SelectField('Category', validators=[DataRequired()], choices=['Video', 'Book', 'Podcast'])
    
    keywords = StringField('Keywords that describe the content of the submitted media. Separate multiple keywords with a comma.', validators= [Length(min=4, max=100)])

    link = StringField('Url / ISBN', validators=[DataRequired()])

    age = IntegerField('*Optional* Tell people your age', validators=[Optional()])

    name = StringField('*Optional* Tell people your first name', validators=[Optional()])

    submit = SubmitField('Submit your media')

    def validate_link(self, link):

        content = Content.query.filter_by(link = link.data).first()
        if content:
            raise ValidationError('Content with the same URL has already been submitted')  

        if self.category.data == "Video":
            pattern = re.compile('(?:https?:\/\/)?(?:youtu\.be\/|(?:www\.|m\.)?youtube\.com\/(?:watch|v|embed)(?:\.php)?(?:\?.*v=|\/))([a-zA-Z0-9\_-]+)')
            match = re.fullmatch(pattern, link.data)
            r = requests.get(link.data)
            
            if not match:
                raise ValidationError('This is not a valid Youtube link')
            
            elif "Video unavailable" in r.text or "Video nicht verfügbar" in r.text:
                raise ValidationError('This video is unavailable')

                      


        elif self.category.data == "Podcast":
            pattern = re.compile(r'[\bhttps://open.\b]*spotify[\b.com\b]*[/:]*episode[/:]*[A-Za-z0-9?=]+')
            match = re.fullmatch(pattern, link.data)
            if not match:
                raise ValidationError('This is not a valid Spotify link')



        elif self.category.data == "Book":                    
            if notisbn(link.data):
                raise ValidationError('This is not a valid ISBN')
                           
            
    

#    def validate_title(self, title):
 #       content = Content.query.filter_by(title = title.data).first()
  #      if content:
   #         raise ValidationError('This title is already taken, please chose a different title')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class FeedbackForm(FlaskForm):
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    submitted_on = DateField('Submit date')
    submit = SubmitField('Submit feedback')