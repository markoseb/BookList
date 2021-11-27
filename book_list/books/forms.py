from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    pub_date = DateTimeField('Data Publikacji', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    pages_number = IntegerField('Numer Stron', validators=[DataRequired()])
    img = StringField('Okładka', validators=[DataRequired()])
    lan = StringField('Język', validators=[DataRequired()])
    submit = SubmitField('Dodaj')
