from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from CuriousFeed.models import Content
#import requests

class SubmitMediaForm(FlaskForm):
    title = StringField('Title', 
                        validators= [DataRequired(), Length(min=4, max=60)])

    category = SelectField('Category', validators=[DataRequired()], choices=['Video', 'Book', 'Podcast'])

    link = StringField('Link', validators=[DataRequired()])

    submit = SubmitField('Submit your media')
    
    

    def validate_link(self, link):
        content = Content.query.filter_by(link = link.data).first()
        if content:
            raise ValidationError('Content with the same link has already been submitted')

        #if category =="Video":
          #  r = requests.get(link.data)
          #  if "Video unavailable" in r.text:
           #     raise ValidationError('Currently only Youtube video links are supported, the submitted link is not a valid Youtube video')

    def validate_title(self, title):
        content = Content.query.filter_by(title = title.data).first()
        if content:
            raise ValidationError('This title is already taken, please chose a different title')

