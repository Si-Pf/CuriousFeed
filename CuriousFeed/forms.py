from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from CuriousFeed.models import Content
import re
import requests



class SubmitMediaForm(FlaskForm):
    title = StringField('Title', 
                        validators= [DataRequired(), Length(min=4, max=60)])

    category = SelectField('Category', validators=[DataRequired()], choices=['Video', 'Book', 'Podcast'])
    
    
    link = StringField('Url', validators=[DataRequired()])

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



        
    

    def validate_title(self, title):
        content = Content.query.filter_by(title = title.data).first()
        if content:
            raise ValidationError('This title is already taken, please chose a different title')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')