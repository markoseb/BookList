from flask import render_template, Blueprint, redirect, request
from book_list.models import Book

core = Blueprint('core', __name__)


@core.route('/index')
def index_redirect():
    return redirect('/')


@core.route('/')
def index():
    '''
    This is the home page view. Use pagination to show
    a Book List.
    '''
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.id).paginate(page=page, per_page=100)
    return render_template('index.html', books=books)
