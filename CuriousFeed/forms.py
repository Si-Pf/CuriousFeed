from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class SubmitMediaForm(FlaskForm):
    title = StringField('Title', 
                        validators= [DataRequired(), Length(min=4, max=60)])

    category = SelectField('Category', validators=[DataRequired()], choices=['Video', 'Book', 'Podcast'])

    link = StringField('Link', validators=[DataRequired()])

    submit = SubmitField('Submit your media')
