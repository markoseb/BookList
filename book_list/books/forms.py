from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired
from flask import flash
from book_list.models import Book
import datetime

dt_string = "2020-12-18"
format = "%Y-%m-%d"
dt_object = datetime.datetime.strptime(dt_string, format)


class BookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    pub_date = DateTimeField('Data Publikacji', validators=[DataRequired()], default=dt_object, format=format)
    isbn = StringField('ISBN', validators=[DataRequired()], default="978-1-56619-909-4")
    pages_number = IntegerField('Numer Stron', validators=[DataRequired()])
    img = StringField('Okładka', validators=[DataRequired()],
                      default="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2FkkVGBn-haDo%2Fmaxresdefault.jpg&f=1&nofb=1")
    lan = StringField('Język', validators=[DataRequired()], default="pl")
    submit = SubmitField('Dodaj')

    def check_isbn(self):
        if Book.query.filter_by(isbn=self.isbn.data).first():
            flash('Książka o podanym ISBN już istnieje!')
            return False
        return True


class SearchBookForm(FlaskForm):
    valuesType = SelectField('Wybierz kryterium', choices=[('all', 'Brak'), ('title', 'Tytuł'), ('author', 'Autor'), ('lan', 'Język')])
    val = StringField('Wartość', validators=[DataRequired()])
    start_date = DateTimeField('Od: ', validators=[DataRequired()], default=dt_object, format=format)
    end_date = DateTimeField('Do:', validators=[DataRequired()], default=dt_object, format=format)
    submit = SubmitField('refresh')
