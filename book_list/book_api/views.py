import requests, json
from dateutil import parser as dataparser
from flask import render_template, Blueprint, flash, request, session
from book_list import db
from book_list.book_api.forms import BookApiForm
from book_list.models import Book


book_api = Blueprint('book_api', __name__)


class gbooks():
    googleapikey = "AIzaSyDI-jiaDDiO77DWJd1SdIa2kUWNHJ9Fa4A"

    def search(self, value):
        parms = {"q": value, 'key': self.googleapikey}
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        rj = r.json()
        return rj["items"]


def bookDecoder(obj):
    obj = obj["volumeInfo"]

    bookdict = {
        "title"     :        obj.get('title', "Brak danych"),
        "author"    :        ','.join(obj.get('authors', [])),
        "pub_date"  :        obj.get('publishedDate', ""),
        "isbn"      :        "Brak danych",
        "link"      :        "empty",
        "language"  :        obj.get('language', ""),
        "pages"     :        0,
    }
    try:
        bookdict.update({
            'isbn'  : obj['industryIdentifiers'][0]['identifier'],
        })
    except:
        pass

    try:
        bookdict.update({
            'link'  : obj["imageLinks"]["thumbnail"],
        })
    except:
        pass

    try:
        bookdict['pages'] = int(obj.get("pageCount",0))
    except:
        pass

    return bookdict


@book_api.route('/bookapi', methods=['GET', 'POST'])
def search():
    form = BookApiForm()
    deactivated_add = False
    books = []
    if form.validate_on_submit():
        bk = gbooks()
        result = bk.search(form.search.data)
        deactivated_add = True
        for dictbook in result:
            book = bookDecoder(dictbook)
            books.append(book)
        if form.submit_all.data:
            for el in books:
                if Book.query.filter_by(isbn=el['isbn']).first():
                    flash(f"Książka o podanym ISBN = {el.isbn} już istnieje!")
                else:
                    bookdb = Book(
                        title=el['title'],
                        author=el['author'],
                        pub_date=dataparser.parse(el['pub_date']),
                        isbn=el['isbn'],
                        pages=el['link'],
                        link=el['language'],
                        language=el['pages'])
                    db.session.add(bookdb)
                    db.session.commit()
    session['books']            = books
    session['deactivated_add'] = deactivated_add
    return render_template('bookapi.html', form=form, books=books, deactivated=deactivated_add)


@book_api.route('/book/<string:book_id>/add', methods=['GET', 'POST'])
def add(book_id):

    if request.method == 'POST':
        for book in session.get('books', None):
            if book.get("isbn", 'default_value') == book_id:
                print(book)
                bookdb = Book(
                    title         = book['title'],
                    author        = book['author'],
                    pub_date      = dataparser.parse(book['pub_date']),
                    isbn          = book['isbn'],
                    pages         = book['link'],
                    link          = book['language'],
                    language      = book['pages'])
                db.session.add(bookdb)
                db.session.commit()

    return render_template('bookapi.html',
                           form=BookApiForm(),
                           books=session.get('books', None),
                           deactivated=session.get('deactivated_add',False))

