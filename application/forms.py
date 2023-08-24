from wtforms import TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from application import utils

languages_choice = []
for key, value in utils.LANGUAGES.items():
    languages_choice.append((key, value))


class MyForm(FlaskForm):
    text_field = TextAreaField('Text', validators=[DataRequired()])
    language_field = SelectField("Language to translate to", choices=languages_choice)
    submit = SubmitField('Create Audio')
