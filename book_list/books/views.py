from flask import render_template, url_for, flash, redirect, Blueprint
from book_list import db
from book_list.models import Book
from book_list.books.forms import BookForm

books = Blueprint('books', __name__)


@books.route('/add/Book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            pub_date=form.pub_date.data,
            isbn=form.isbn.data,
            link=form.img.data,
            language=form.lan.data)

        db.session.add(book)
        db.session.commit()
        flash("Book Added")
        return redirect(url_for('core.index'))

    return render_template('addbook.html', form=form)
