from flask import render_template, Blueprint, redirect

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
    return render_template('index.html')
