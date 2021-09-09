from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp
from CuriousFeed.models import Content



class SubmitMediaForm(FlaskForm):
    title = StringField('Title', 
                        validators= [DataRequired(), Length(min=4, max=60)])

    category = SelectField('Category', validators=[DataRequired()], choices=['Video', 'Book', 'Podcast'])
    
    
    link = StringField('Link', validators=[DataRequired(), Regexp('(?:https?:\/\/)?(?:youtu\.be\/|(?:www\.|m\.)?youtube\.com\/(?:watch|v|embed)(?:\.php)?(?:\?.*v=|\/))([a-zA-Z0-9\_-]+)|(?:https?:\/\/)?spotify\.com\/|(?:www\.|m\.)?spotify\.com\/(episode)', message="Currently only Youtube video links and spotify podcast links are supported, the submitted link is not valid")])
    
    
    submit = SubmitField('Submit your media')
    


    def validate_link(self, link):
        content = Content.query.filter_by(link = link.data).first()
        if content:
            raise ValidationError('Content with the same link has already been submitted')

       

    def validate_title(self, title):
        content = Content.query.filter_by(title = title.data).first()
        if content:
            raise ValidationError('This title is already taken, please chose a different title')

