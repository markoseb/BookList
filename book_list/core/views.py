from flask import render_template, Blueprint, redirect, request
from book_list.models import Book
from book_list.books.forms import SearchBookForm

core = Blueprint('core', __name__)


@core.route('/index')
def index_redirect():
    return redirect('/')


def search_book(i, val, books):
    switcher = {

        "title": books.filter(Book.title.like('%' + val + '%')),

        "author": books.filter(Book.author.like('%' + val + '%')),

        "lan": books.filter(Book.lan.like('%' + val + '%')),

        "all": books

    }

    return switcher.get(i, "Brak wyników!")


@core.route('/', methods=['GET', 'POST'])
def index():
    '''
    This is the home page view. Use pagination to show
    a Book List.
    '''
    page = request.args.get('page', 1, type=int)
    books = Book.query
    searchform = SearchBookForm()
    if searchform.validate_on_submit():
        val = searchform.val.data
        name = searchform.valuesType.data
        books = search_book(name, val, books)
    books = books.order_by(Book.id).paginate(page=page, per_page=100)
    return render_template('index.html', books=books, searchform=searchform)
