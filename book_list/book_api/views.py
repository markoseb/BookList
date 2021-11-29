import requests
from dateutil import parser as dataparser
from flask import render_template, Blueprint, redirect, url_for, flash

from book_list import db
from book_list.book_api.forms import BookApiForm
from book_list.models import Book

book_api = Blueprint('book_api', __name__)


class gbooks():
    googleapikey = "xxx"

    def search(self, value):
        parms = {"q": value, 'key': self.googleapikey}
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        rj = r.json()
        return rj["items"]


def bookDecoder(obj):
    obj = obj["volumeInfo"]

    bookdict = {
        "title": "Brak danych",
        "author": "Brak danych",
        "pub_date": "",
        "isbn": "Brak danych",
        "link": "empty",
        "language": "Brak danych",
        "pages": 0
    }
    if 'title' in obj:
        bookdict['title'] = obj['title']

    if 'authors' in obj:
        bookdict['author'] = ''.join(obj['authors'])

    if 'publishedDate' in obj:
        bookdict['pub_date'] = obj['publishedDate']

    if 'industryIdentifiers' in obj and 'identifier' in obj['industryIdentifiers'][0]:
        bookdict['isbn'] = obj['industryIdentifiers'][0]['identifier']

    if 'language' in obj:
        bookdict['language'] = obj['language']

    if 'pageCount' in obj:
        bookdict['pages'] = int(obj['pageCount'])

    if 'imageLinks' in obj and 'thumbnail' in obj['imageLinks']:
        bookdict['link'] = obj["imageLinks"]["thumbnail"]

    book = Book(
        title=bookdict['title'],
        author=bookdict['author'],
        pub_date=dataparser.parse(bookdict['pub_date']),
        isbn=bookdict['isbn'],
        link=bookdict['link'],
        language=bookdict['language'],
        pages=bookdict['pages'])

    return book


@book_api.route('/bookapi', methods=['GET', 'POST'])
def search():
    form = BookApiForm()
    deactivated_add = False
    books = []

    if form.validate_on_submit():
        bk = gbooks()
        result = bk.search(form.search.data)
        deactivated_add = True
        for jsnbook in result:
            book = bookDecoder(jsnbook)
            books.append(book)
        if form.submit_add.data:
            for el in books:
                if Book.query.filter_by(isbn=el.isbn).first():
                    flash(f"Książka o podanym ISBN = {el.isbn} już istnieje!")
                else:
                    db.session.add(el)
                    db.session.commit()

    return render_template('bookapi.html', form=form, books=books, deactivated=deactivated_add)


@book_api.route('/book/<string:book_parm>/delete', methods=['GET', 'POST'])
def add(book_parm):
    # book = Book(
    #     title=book_parm[0],
    #     author=book_parm[1],
    #     pub_date=dataparser.parse(book_parm[2]),
    #     isbn=book_parm[3],
    #     pages=book_parm[4],
    #     link=book_parm[5],
    #     language=book_parm[6])
    # db.session.add(book)
    # db.session.commit()

    # Python code to convert string to list

    # li = book_parm.split(",")

    print(book_parm)
    return redirect(url_for('core.index'))
