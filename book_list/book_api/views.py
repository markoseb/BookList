import requests
from flask import render_template, Blueprint, request, session

from book_list.book_api.forms import BookApiForm
from book_list.models import Book
from book_list import config
book_api = Blueprint('book_api', __name__)


class gbooks():
    googleapikey = config["GOOGLE_API"]["KEY"]

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
        "lan"       :        obj.get('language', ""),
        "pages_number"     :        0,
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
        bookdict['pages_number'] = int(obj.get("pageCount",0))
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
                Book(**el).save_to_db()


    session['books']           = books
    session['deactivated_add'] = deactivated_add
    return render_template('bookapi.html', form=form, books=books, deactivated=deactivated_add)


@book_api.route('/book/<string:book_id>/add', methods=['GET', 'POST'])
def add(book_id):
    if request.method == 'POST':
        for book in session.get('books', None):
            if book.get("isbn", 'default_value') == book_id:
                Book(**book).save_to_db()

    return render_template('bookapi.html',
                           form=BookApiForm(),
                           books=session.get('books', None),
                           deactivated=session.get('deactivated_add', False))
