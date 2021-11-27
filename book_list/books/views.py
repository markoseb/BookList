from flask import render_template, url_for, flash, redirect, Blueprint, request
from book_list import db
from book_list.models import Book
from book_list.books.forms import BookForm

books = Blueprint('books', __name__)


@books.route('/add/Book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()

    if form.validate_on_submit() and form.check_isbn():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            pub_date=form.pub_date.data,
            isbn=form.isbn.data,
            link=form.img.data,
            language=form.lan.data,
            pages=form.pages_number.data)

        db.session.add(book)
        db.session.commit()
        flash("Dodano książkę!")
        return redirect(url_for('core.index'))

    return render_template('addbook.html', form=form)


@books.route('/book/<int:book_id>', methods=["GET", "POST"])
def update(book_id):
    # grab the requested blog post by id number or return 404
    book = Book.query.get_or_404(book_id)
    form = BookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.pub_date = form.pub_date.data
        book.isbn = form.isbn.data
        book.link = form.img.data
        book.lan = form.lan.data
        book.pages_number = form.pages_number.data
        db.session.commit()
        flash("Zmiana zatwierdzona!")
        return redirect(url_for('core.index'))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.pub_date.data = book.pub_date
        form.isbn.data = book.isbn
        form.img.data = book.link
        form.lan.data = book.lan
        form.pages_number.data = book.pages_number

    return render_template('addbook.html', form=form)


@books.route('/book/<int:book_id>/delete', methods=["POST"])
def delete(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()
    flash('Usuniętą Książkę')
    return redirect(url_for('core.index'))
