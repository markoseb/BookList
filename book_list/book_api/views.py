import requests
from flask import render_template, Blueprint

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
        "link": "",
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
        pub_date=bookdict['pub_date'],
        isbn=bookdict['isbn'],
        link=bookdict['link'],
        language=bookdict['language'],
        pages=bookdict['pages'])

    return book


@book_api.route('/bookapi', methods=['GET', 'POST'])
def search():
    form = BookApiForm()
    books = []

    if form.validate_on_submit():
        bk = gbooks()
        result = bk.search(form.search.data)

        for jsnbook in result:
            book = bookDecoder(jsnbook)
            books.append(book)

    return render_template('bookapi.html', form=form, books=books)
