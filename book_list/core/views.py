from flask import render_template, Blueprint, redirect, request

from book_list.books.forms import SearchBookForm
from book_list.models import Book

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

    return switcher.get(i, books)


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
        if searchform.use_data.data:
            data_str = searchform.start_date.data
            data_end = searchform.end_date.data
            books = books.filter(Book.pub_date.between(data_str, data_end))

    books = books.order_by(Book.id).paginate(page=page, per_page=100)
    return render_template('index.html', books=books, searchform=searchform)
