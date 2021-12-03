from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BookApiForm(FlaskForm):
    search          = StringField(validators=[DataRequired()])
    submit_search   = SubmitField('Szukaj')
    submit_all      = SubmitField('Dodaj wszystkie!')
